# coding:utf-8
from django.contrib.syndication.views import Feed
from .models import Post

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "百花争鸣"

    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 显示在聚合阅读器上的描述信息
    description = "各种类型的文章"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):

        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body
