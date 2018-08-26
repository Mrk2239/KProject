#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: urls.py
@time: 2018/7/7 0007 上午 11:51

'''


from django.conf.urls import url

from comments.views import post_comment,CommentCreateView

urlpatterns = [

    #url(r'^post_comment/(?P<pk>\d+)/$',post_comment,name='post_comment' ),
    url(r'^post_comment/(?P<pk>\d+)/$',CommentCreateView.as_view(),name='post_comment' ),
]