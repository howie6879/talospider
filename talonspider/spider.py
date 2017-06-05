#!/usr/bin/env python
from talonspider.utils import get_logger


class Spider():
    """
    Spider class
    """
    name = 'talonspider'
    start_url = ''

    @classmethod
    def start(cls):
        pass

    @property
    def logger(self):
        logger = get_logger(self.name)
        return logger
