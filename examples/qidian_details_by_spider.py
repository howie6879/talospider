# -*- coding:utf-8 -*-
# !/usr/bin/env python
import time
from pprint import pprint
from talonspider import Spider, Item, TextField, AttrField


# 定义继承自item的Item类
class QidianItem(Item):
    title = TextField(css_select='.book-info>h1>em')
    author = TextField(css_select='a.writer')
    # 当提取的值是属性的时候，要定义AttrField
    cover = AttrField(css_select='a#bookImg>img', attr='src')
    abstract = TextField(css_select='div.book-intro>p')
    tag = TextField(css_select='span.blue')
    latest_chapter = TextField(css_select='div.detail>p.cf>a')
    latest_chapter_time = TextField(css_select='div.detail>p.cf>em')

    # 这里可以二次对获取的目标值进行处理，比如替换、清洗等
    def tal_title(self, title):
        # Clean your target value
        return title

    def tal_cover(self, cover):
        return 'http:' + cover

    # 当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
    def tal_tag(self, ele_tag):
        return '#'.join([i.text for i in ele_tag])

    def tal_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace(u'今天', str(time.strftime("%Y-%m-%d ", time.localtime()))).replace(u'昨日', str(
            time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60))))


class QidianSpider(Spider):
    start_urls = ['http://book.qidian.com/info/1004608738', 'http://book.qidian.com/info/3602691',
                  'http://book.qidian.com/info/3347595', 'http://book.qidian.com/info/1887208']
    request_config = {
        'RETRIES': 3,
        'TIMEOUT': 10
    }
    pool_size = 4
    set_mul = True

    def parse(self, html):
        item_data = QidianItem.get_item(html=html)
        # 这里可以保存获取的item
        # for python 2.7
        # import json
        # item_data = json.dumps(item_data, ensure_ascii=False)
        pprint(item_data)


if __name__ == '__main__':
    QidianSpider.start()
