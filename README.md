## talonspider

### 1.为什么写这个？

在完善owllook这个项目的时候，需要展示小说排行榜，但又不想动用比较大的框架来进行爬取

因此针对这个需求写了`talonspider`:

- 1.针对单页面的item提取 - 具体介绍点[这里](./docs/item.md)
- 2.spider模块 - TODO

### 2.介绍&&使用

#### 2.1.item

这个模块是可以独立使用的，对于一些请求比较简单的网站（比如只需要`get`请求），单单只用这个模块就可以快速地编写出你想要的爬虫，比如：

##### 2.1.1.单页面单目标

比如要获取这个网址http://book.qidian.com/info/1004608738 的书籍信息，封面等信息，可直接这样写：

```python
import time
from talonspider import Item, TextField, AttrField
from pprint import pprint

class TestSpider(Item):
    title = TextField(css_select='.book-info>h1>em')
    author = TextField(css_select='a.writer')
    cover = AttrField(css_select='a#bookImg>img', attr='src')

    def tal_title(self, title):
        return title

    def tal_cover(self, cover):
        return 'http:' + cover

if __name__ == '__main__':
    item_data = TestSpider.get_item(url='http://book.qidian.com/info/1004608738')
    pprint(item_data)
```

具体见[qidian_details.py](./examples/qidian_details.py)

##### 2.1.1.单页面多目标

比如获取[豆瓣250电影]([https://movie.douban.com/top250](https://movie.douban.com/top250))首页展示的25部电影，这一个页面有25个目标，可直接这样写：

```python
from talonspider import Item, TextField, AttrField
from pprint import pprint

# 定义继承自item的爬虫类
class DoubanSpider(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    def tal_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])

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
```

具体见[douban_page.py](./examples/douban_page.py)

### 说明

学习之作，待完善的地方还有很多。