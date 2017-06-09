#!/usr/bin/env python
import logging
import random
import time
import os
import sys
from datetime import datetime

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


def get_logger(name):
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    logger = logging.getLogger(name)
    return logger


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(_get_data('user_agents.txt', USER_AGENT))


def get_domain(url):
    """
    Get a domain from url
    :param url:
    :return: domain
    """
    domain = urlparse(url).netloc
    return domain


def _get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data


class Delay():
    """
    Set delay time
    """

    def __init__(self):
        self.domains = {}

    def sleep(self, url, delay_time):
        domain = get_domain(url)
        last_accessed = self.domains.get(domain)
        if delay_time > 0 and last_accessed is not None:
            sleep_seconds = delay_time - (datetime.now() - last_accessed).seconds
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        self.domains[domain] = datetime.now()
        print(self.domains)
