#!/usr/bin/env python
import requests


class Request():
    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 60
    }

    def __init__(self, url, method='GET', allow_redirects=False, request_config=None, params=None, headers=None,
                 proxies=None, cookies=None, callback=None):
        self.url = url
        self.method = method.upper()
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
        self.callback = callback

    def __call__(self, url):
        pass

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)
