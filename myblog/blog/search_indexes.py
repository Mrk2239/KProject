#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: search_indexes.py
@time: 2018/7/8 0008 下午 10:05

'''
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()