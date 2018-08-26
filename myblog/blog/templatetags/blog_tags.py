#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: blog_tags.py
@time: 2018/7/7 0007 下午 5:23

'''
from django import template
from django.db.models import Count

from blog.models import Post, Category, Tag

register = template.Library()

#最新文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

#归档(日期)
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

#分类(加注释统计数量)
@register.simple_tag
def get_categories():
    #return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#标签云
@register.simple_tag
def get_tags():
    return Tag.objects.all()