#!/usr/bin/env python
"""
 Created by howie.hu at  17-10-11.
"""
import os
import logging

from urllib.parse import urljoin

from talospider import AttrField, Request, Spider, Item
from talospider.utils import get_random_user_agent


class BaiduImgItem(Item):
    """
    定义继承自item的Item类
    """
    img_url = AttrField(css_select='img.BDE_Image', attr='src')

    def tal_img_url(self, ele_img_url):
        return [i.get('src').strip() for i in ele_img_url]


class BaiduImgSpider(Spider):
    start_urls = ['https://tieba.baidu.com/p/5062084136']
    img_path = 'data/'
    set_mul = True
    headers = {
        "User-Agent": get_random_user_agent()
    }

    def parse(self, res):
        # 将html转化为etree
        etree = self.e_html(res.html)
        # 提取目标值生成新的url
        pages = list(set(i.get('href') for i in etree.cssselect('li.pb_list_pager>a')))

        pages.append(self.start_urls[0])
        for page in pages:
            url = urljoin(self.start_urls[0], page)
            yield Request(url, headers=self.headers, callback=self.parse_item)

    def parse_item(self, res):
        items_data = BaiduImgItem.get_item(html=res.html)
        img_urls = items_data['img_url']
        for index, url in enumerate(img_urls):
            yield Request(url, headers=self.headers, callback=self.save_img, file_type='bytes',
                          extra_value={'index': index})

    def save_img(self, res):
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)
        img_name = str(res.extra_value['index']) + "_" + res.url[-10:].replace('/', '-')
        with open(self.img_path + img_name, 'wb') as file:
            file.write(res.html)
            logging.info('Img downloaded successfully in {dir}'.format(dir=self.img_path + img_name))


if __name__ == '__main__':
    BaiduImgSpider.start()
