## talonspider - spider

#### 2.1.spider

当需要爬取有层次的页面时，这里以爬取豆瓣250全部电影为例子，这时候`spider`部分就派上了用场：

```python
# !/usr/bin/env python
from talonspider import Spider, Item, TextField, AttrField, Request
from talonspider.utils import get_random_user_agent


# 定义继承自item的爬虫类
class DoubanItem(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    def tal_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    # 定义起始url，必须
    start_urls = ['https://movie.douban.com/top250']
    # requests配置
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
	# 解析函数 必须有
    def parse(self, html):
        # 将html转化为etree
        etree = self.e_html(html)
        # 提取目标值生成新的url
        pages = [i.get('href') for i in etree.cssselect('.paginator>a')]
        pages.insert(0, '?start=0&filter=')
        headers = {
            "User-Agent": get_random_user_agent()
        }
        for page in pages:
            url = self.start_urls[0] + page
            yield Request(url, request_config=self.request_config, headers=headers, callback=self.parse_item)

    def parse_item(self, html):
        items_data = DoubanItem.get_items(html=html)
        # result = []
        for item in items_data:
            # result.append({
            #     'title': item.title,
            #     'cover': item.cover,
            #     'abstract': item.abstract,
            # })
            # 保存
            with open('douban250.txt', 'a+') as f:
                f.writelines(item.title + '\n')


if __name__ == '__main__':
    DoubanSpider.start()

```

控制台：

```shell
/Users/howie/anaconda3/envs/work3/bin/python /Users/howie/Documents/programming/python/git/talonspider/examples/douban_page_by_spider.py
2017-06-07 23:17:30,346 - talonspider - INFO: talonspider started
2017-06-07 23:17:30,693 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250
2017-06-07 23:17:31,074 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=25&filter=
2017-06-07 23:17:31,416 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=50&filter=
2017-06-07 23:17:31,853 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=75&filter=
2017-06-07 23:17:32,523 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=100&filter=
2017-06-07 23:17:33,032 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=125&filter=
2017-06-07 23:17:33,537 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=150&filter=
2017-06-07 23:17:33,990 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=175&filter=
2017-06-07 23:17:34,406 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=200&filter=
2017-06-07 23:17:34,787 - talonspider_requests - INFO: GET a url: https://movie.douban.com/top250?start=225&filter=
2017-06-07 23:17:34,809 - talonspider - INFO: Time usage：0:00:04.462108

Process finished with exit code 0
```

此时当前目录会生成`douban250.txt`，具体见[douban_page_by_spider.py](../examples/douban_page_by_spider.py)。
