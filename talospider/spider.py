# -*- coding:utf-8 -*-
# !/usr/bin/env python
from multiprocessing import cpu_count, Pool, freeze_support
from datetime import datetime
from lxml import etree
from talospider.utils import get_logger
from talospider import Request


class Spider():
    """
    Spider class
    """
    name = 'talospider'
    start_urls = []
    request_config = None
    set_mul = False
    pool_size = cpu_count()

    def __init__(self):
        setattr(self, 'name', self.name)
        if not getattr(self, 'start_urls', None):
            raise ValueError('spider must have a start_urls')

    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url,
                          request_config=getattr(self, 'request_config'),
                          headers=getattr(self, 'headers', None),
                          callback=self.parse)

    def parse(self, res):
        raise NotImplementedError

    @classmethod
    def start(cls):
        """
        Start crawling
        """
        spider_instance = cls()
        spider_instance.logger.info('{name} started'.format(name=cls.name))
        start = datetime.now()
        gen_request = list(spider_instance.start_request())
        if cls.set_mul:
            try:
                cls.gen_call(gen_request=gen_request)
            except Exception as e:
                spider_instance.logger.info(e)
                cls.except_gen_call(gen_request=gen_request)
        else:
            cls.except_gen_call(gen_request=gen_request)
        spider_instance.logger.info('Time usage：{seconds}'.format(seconds=(datetime.now() - start)))

    @classmethod
    def gen_call(cls, gen_request):
        freeze_support()
        results = []
        pool = Pool(cls.pool_size)
        for each_main_request in gen_request:
            result = pool.apply_async(each_main_request)
            results.append(result)
        pool.close()
        pool.join()
        for result in results:
            each_callback = result.get()
            if each_callback is not None:
                cls.gen_call(gen_request=each_callback)

    @classmethod
    def except_gen_call(cls, gen_request):
        for each_request in gen_request:
            callback = each_request()
            if callback is not None:
                cls.except_gen_call(callback)

    @property
    def logger(self):
        logger = get_logger(self.name)
        return logger

    def e_html(self, html):
        return etree.HTML(html)
