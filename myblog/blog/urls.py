#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: urls.py
@time: 2018/7/7 0007 上午 11:51

'''


from django.conf.urls import url

from blog.views import PostListView, post_detail, ArchivesListView, CategoryListView, PostDetailView, TagListView, \
    search,index,PostDetailViewPrime

app_name = 'blog'

urlpatterns = [

    url(r'^index/$',PostListView.as_view(),name='index' ),
    #url(r'^index/$',index,name='index' ),
    #url(r'^post_detail/(?P<pk>\d+)/$',post_detail,name='post_detail' ),
    url(r'^post_detail/(?P<pk>\d+)/$',PostDetailViewPrime.as_view(),name='post_detail' ),
    url(r'^tags/(?P<pk>\d+)/$',TagListView.as_view(),name='tags' ),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$',ArchivesListView.as_view(),name='archives' ),
    #CategoryListView
    url(r'^category/(?P<pk>\d+)/$',CategoryListView.as_view(),name='category' ),
    #url(r'^search/$',search,name='search')
]