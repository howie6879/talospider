# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import cchardet
import requests

from talospider.utils import Logger


class Request():
    """
    Request class for each request
    """
    name = 'downloading'

    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 30
    }

    METHOD = ['GET', 'POST']

    def __init__(self, url, method='GET', params=None, data=None, request_config=None, headers=None, proxies=None,
                 cookies=None, verify=False, callback=None, extra_value={}, file_type='text', **kwargs):
        self.url = url
        self.method = method.upper()
        if self.method not in self.METHOD:
            raise ValueError('%s method is not supported' % self.method)
        if request_config and isinstance(request_config, dict):
            self.request_config = request_config
        elif request_config and not isinstance(request_config, dict):
            raise ValueError(
                "request_config must be a dict type, just like request_config = {'RETRIES':3,'DELAY':0,'TIMEOUT':60}")
        else:
            self.request_config = self.REQUEST_CONFIG
        self.params = params
        self.data = data
        self.headers = headers
        self.proxies = proxies
        self.cookies = cookies
        self.verify = verify
        self.callback = callback
        self.extra_value = extra_value
        self.file_type = file_type
        self.kwargs = kwargs
        self.logger = Logger(name=self.name)

    def __call__(self):
        if self.request_config.get('DELAY', 0) > 0:
            time.sleep(self.request_config.get('DELAY', 0))
        res = self.download(url=self.url,
                            method=self.method,
                            params=self.params,
                            data=self.data,
                            headers=self.headers,
                            proxies=self.proxies,
                            cookies=self.cookies,
                            verify=self.verify,
                            num_retries=self.request_config.get('RETRIES', 3),
                            extra_value=self.extra_value,
                            file_type=self.file_type,
                            **self.kwargs)
        self.logger.info("{method}: {url}".format(
            method=self.method,
            url=self.url))
        if self.callback is None:
            return res
        if self.callback(res=res) is not None:
            return list(self.callback(res=res))

    def download(self, url, method, headers, proxies, params, data, cookies, verify, num_retries, extra_value,
                 file_type, **kwargs):
        text = None
        try:
            if not verify:
                requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            if method.lower() == 'get':
                response = requests.get(
                    url=url,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    cookies=cookies,
                    timeout=self.request_config.get('TIMEOUT', 30),
                    verify=verify,
                    **kwargs
                )
            else:
                response = requests.post(
                    url=url,
                    data=data,
                    headers=headers,
                    proxies=proxies,
                    cookies=cookies,
                    timeout=self.request_config.get('TIMEOUT', 30),
                    verify=verify,
                    **kwargs
                )
            if num_retries > 0 and 500 <= response.status_code < 600:
                self.logger.info('Retrying url: %s' % url)
                return self.download(url=url,
                                     method=method,
                                     params=params,
                                     data=data,
                                     headers=headers,
                                     proxies=proxies,
                                     cookies=cookies,
                                     verify=verify,
                                     num_retries=num_retries - 1,
                                     file_type=file_type,
                                     extra_value=extra_value,
                                     **kwargs)

            response.raise_for_status()
            if file_type == 'bytes':
                text = response.content
            elif file_type == 'json':
                text = response.json()
            elif file_type == 'raw':
                text = response.raw
            elif file_type == 'text':
                content = response.content
                charset = cchardet.detect(content)
                text = content.decode(charset['encoding'])
        except requests.exceptions.MissingSchema:
            self.logger.error(
                "Invalid URL '{url}': No schema supplied. Perhaps you meant http://{url} ?".format(url=url))
        except requests.exceptions.HTTPError as e:
            self.logger.error(e)
        except requests.exceptions.ConnectionError:
            self.logger.error('%s excepted a ConnectionError' % url)
        except Exception as e:
            self.logger.exception(e)
        return type('Response', (),
                    {'html': text, 'url': url, 'extra_value': extra_value}) if text is not None else None



    def __str__(self):
        return "<%s %s>" % (self.method, self.url)
