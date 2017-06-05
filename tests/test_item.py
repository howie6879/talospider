#!/usr/bin/env python
import unittest
from talonspider import TextField, AttrField, Item

HTML = """

<!DOCTYPE html>
<head>
    <title>豆瓣电影TOP250</title>
</head>
<body>
<ol class="grid_view">
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">1</em>
                    <a href="https://movie.douban.com/subject/1292052/">
                        <img alt="肖申克的救赎" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p480747492.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1292052/" class="">
                            <span class="title">肖申克的救赎</span>
                                    <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
                                <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
                            1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
                        </p>

                        
                        <div class="star">
                                <span class="rating5-t"></span>
                                <span class="rating_num" property="v:average">9.6</span>
                                <span property="v:best" content="10.0"></span>
                                <span>827737人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">希望让人自由。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">2</em>
                    <a href="https://movie.douban.com/subject/1295644/">
                        <img alt="这个杀手不太冷" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p511118051.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1295644/" class="">
                            <span class="title">这个杀手不太冷</span>
                                    <span class="title">&nbsp;/&nbsp;Léon</span>
                                <span class="other">&nbsp;/&nbsp;杀手莱昂  /  终极追杀令(台)</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 吕克·贝松 Luc Besson&nbsp;&nbsp;&nbsp;主演: 让·雷诺 Jean Reno / 娜塔丽·波特曼 ...<br>
                            1994&nbsp;/&nbsp;法国&nbsp;/&nbsp;剧情 动作 犯罪
                        </p>

                        
                        <div class="star">
                                <span class="rating45-t"></span>
                                <span class="rating_num" property="v:average">9.4</span>
                                <span property="v:best" content="10.0"></span>
                                <span>794131人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">怪蜀黍和小萝莉不得不说的故事。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">3</em>
                    <a href="https://movie.douban.com/subject/1291546/">
                        <img alt="霸王别姬" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910813120.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1291546/" class="">
                            <span class="title">霸王别姬</span>
                                <span class="other">&nbsp;/&nbsp;再见，我的妾  /  Farewell My Concubine</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 陈凯歌 Kaige Chen&nbsp;&nbsp;&nbsp;主演: 张国荣 Leslie Cheung / 张丰毅 Fengyi Zha...<br>
                            1993&nbsp;/&nbsp;中国大陆 香港&nbsp;/&nbsp;剧情 爱情 同性
                        </p>

                        
                        <div class="star">
                                <span class="rating5-t"></span>
                                <span class="rating_num" property="v:average">9.5</span>
                                <span property="v:best" content="10.0"></span>
                                <span>591518人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">风华绝代。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
</body>
</html>
"""


# 定义继承自item的爬虫类
class DoubanItemsSpider(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    def tal_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanItemSpider(Item):
    title = TextField(css_select='head title')

    def tal_title(self, title):
        return title


class TestItem(unittest.TestCase):
    def test_get_items(self):
        items_data = DoubanItemsSpider.get_items(html=HTML)
        self.assertEqual(items_data[0].title, '肖申克的救赎/The Shawshank Redemption')

    def test_get_item(self):
        item_data = DoubanItemSpider.get_item(html=HTML)
        self.assertEqual(item_data['title'], '豆瓣电影TOP250')


if __name__ == '__main__':
    unittest.main()
