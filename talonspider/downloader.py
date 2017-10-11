#!/usr/bin/env python
import requests
import cchardet
import time

from talonspider.utils import get_logger


class Request():
    """
    Request class for each request
    """
    name = 'talonspider_requests'

    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 30
    }

    METHOD = ['GET', 'POST']

    def __init__(self, url, method='GET', allow_redirects=True, request_config=None, params=None, headers=None,
                 proxies=None, cookies=None, verify=False, callback=None, extra_value={}, file_type='text'):
        self.url = url
        self.method = method.upper()
        if self.method not in self.METHOD:
            raise ValueError('%s method is not supported' % self.method)
        self.allow_redirects = allow_redirects
        if request_config and isinstance(request_config, dict):
            self.request_config = request_config
        elif request_config and not isinstance(request_config, dict):
            raise ValueError(
                "request_config must be a dict type, just like request_config = {'RETRIES':3,'DELAY':0,'TIMEOUT':60}")
        else:
            self.request_config = self.REQUEST_CONFIG
        self.params = params
        self.headers = headers
        self.proxies = proxies
        self.cookies = cookies
        self.verify = verify
        self.callback = callback
        self.extra_value = extra_value
        self.file_type = file_type

    def __call__(self):
        if self.request_config.get('DELAY', 0) > 0:
            time.sleep(self.request_config.get('DELAY', 0))
        res = self.download(url=self.url,
                            method=self.method,
                            allow_redirects=self.allow_redirects,
                            params=self.params,
                            headers=self.headers,
                            proxies=self.proxies,
                            cookies=self.cookies,
                            verify=self.verify,
                            num_retries=self.request_config.get('RETRIES', 3),
                            extra_value=self.extra_value,
                            file_type=self.file_type)
        get_logger(self.name).info("{method} a url: {url}".format(
            method=self.method,
            url=self.url))
        if self.callback(res=res) is not None:
            return list(self.callback(res=res))

    def download(self, url, method, allow_redirects, params, headers, proxies, cookies, verify, num_retries,
                 extra_value, file_type):
        text = None
        try:
            if not verify:
                requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            if method == 'GET':
                response = requests.get(
                    url=url,
                    allow_redirects=allow_redirects,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    cookies=cookies,
                    timeout=self.request_config.get('TIMEOUT', 30),
                    verify=verify
                )
            else:
                response = requests.post(
                    url=url,
                    allow_redirects=allow_redirects,
                    data=params,
                    headers=headers,
                    proxies=proxies,
                    cookies=cookies,
                    timeout=self.request_config.get('TIMEOUT', 30),
                    verify=verify
                )
            if num_retries > 0 and 500 <= response.status_code < 600:
                get_logger(self.name).info('Retrying url: %s' % url)
                return self.download(url=url,
                                     method=method,
                                     allow_redirects=allow_redirects,
                                     params=params,
                                     headers=headers,
                                     proxies=proxies,
                                     cookies=cookies,
                                     verify=verify,
                                     num_retries=num_retries - 1,
                                     file_type=file_type,
                                     extra_value=extra_value)
            response.raise_for_status()
            if file_type == 'bytes':
                text = response.content
            elif file_type == 'text':
                content = response.content
                charset = cchardet.detect(content)
                text = content.decode(charset['encoding'])
        except requests.exceptions.MissingSchema:
            get_logger(self.name).error(
                "Invalid URL '{url}': No schema supplied. Perhaps you meant http://{url} ?".format(url=url))
        except requests.exceptions.HTTPError as e:
            get_logger(self.name).error(e)
        except requests.exceptions.ConnectionError:
            get_logger(self.name).error('%s excepted a ConnectionError' % url)
        except Exception as e:
            get_logger(self.name).exception(e)
        return type('Response', (),
                    {'html': text, 'url': url, 'extra_value': extra_value}) if text is not None else None

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)
