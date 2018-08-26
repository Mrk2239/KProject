#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: forms.py
@time: 2018/7/7 0007 下午 8:37

'''
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'url','text']