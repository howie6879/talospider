#!/usr/bin/env python
from talonspider.utils import get_logger


class Spider():
    """
    Spider class
    """
    name = 'talonspider'
    start_urls = []

    def __init__(self):
        if not getattr(self, 'start_urls', None):
            raise ValueError('spider must have a start_urls')

    @classmethod
    def start(cls):
        """
        Start crawling
        """
        cls().logger.info('{name} started'.format(name=cls.name))
        print(cls.start_urls)

    @property
    def logger(self):
        logger = get_logger(self.name)
        return logger
