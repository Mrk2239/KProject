#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: forms.py
@time: 2018/7/15 0015 下午 8:33

'''
from django.contrib.auth.forms import UserCreationForm

from users.models import User
from  django import forms

class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ('username','email','nickname','headshot','signature')
        fields = ('email',)

