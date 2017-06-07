#!/usr/bin/env python
import logging
import random
import os


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