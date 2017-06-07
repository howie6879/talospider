# -*- coding:utf-8 -*-
# !/usr/bin/env python
from datetime import datetime
from lxml import etree
from talonspider.utils import get_logger
from talonspider import Request


class Spider():
    """
    Spider class
    """
    name = 'talonspider'
    start_urls = []
    request_config = None

    def __init__(self):
        setattr(self, 'name', self.name)
        if not getattr(self, 'start_urls', None):
            raise ValueError('spider must have a start_urls')

    def start_request(self):
        for url in self.start_urls:
            yield Request(url, request_config=getattr(self, 'request_config'), callback=self.parse)

    def parse(self, html):
        raise NotImplementedError

    @classmethod
    def start(cls):
        """
        Start crawling
        """
        spider_instance = cls()
        spider_instance.logger.info('{name} started'.format(name=cls.name))
        start = datetime.now()
        request_instance = spider_instance.start_request()
        for each_request in request_instance:
            each_request()
        spider_instance.logger.info('Time usage：{seconds}'.format(seconds=(datetime.now() - start)))

    @property
    def logger(self):
        logger = get_logger(self.name)
        return logger

    def e_html(self, html):
        return etree.HTML(html)
