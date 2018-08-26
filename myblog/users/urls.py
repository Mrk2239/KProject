#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: urls.py
@time: 2018/7/15 0015 下午 8:47

'''
from django.conf.urls import url

from users.views import register,UserUpdateView
app_name = 'users'
urlpatterns = [
    url(r'^register/',register,name='register'),
    url(r'^user_update/(?P<pk>\d+)/$',UserUpdateView.as_view(),name='user_update'),

]