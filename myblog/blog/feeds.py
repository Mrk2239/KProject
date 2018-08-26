#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: feeds.py
@time: 2018/7/8 0008 下午 7:56

'''
from django.contrib.syndication.views import Feed
from .models import Post

class AllPostRssFeed(Feed):
    #显示在聚合阅读器上的标题

    title = 'Mr.k博客'

    #通过聚合阅读器跳转到网址的地址

    link='/blog/index/'

    #描述信息
    description = 'Mr.k博客rss订阅'

    #需要显示的条目
    def items(self):
        return Post.objects.all()

    #显示的条目的标题
    def item_title(self, item):
        return '[%s]%s' % (item.category,item.title)

    #条目的内容描述
    def item_description(self, item):
        return item.content

