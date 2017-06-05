# -*- coding:utf-8 -*-
# !/usr/bin/env python
from talonspider import Item, TextField, AttrField
from pprint import pprint


# 定义继承自item的爬虫类
class DoubanSpider(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    def tal_title(self, title):
        if isinstance(title, str) or isinstance(title, unicode):
            return title
        else:
            return ''.join([i.text.strip().replace(u'\xa0', '') for i in title])


if __name__ == '__main__':
    items_data = DoubanSpider.get_items(url='https://movie.douban.com/top250')
    result = []
    for item in items_data:
        result.append({
            'title': item.title,
            'cover': item.cover,
            'abstract': item.abstract,
        })
    pprint(result)
