#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: utils.py
@time: 2018/7/14 0014 下午 9:22

'''
import math
'''
1   2   3   4   5   6   7   8   9   10
    2   3   4   5   6   7   8   9   10  11
        3   4   5   6   7   8   9   10  11  12
            4   5   6   7   8   9   10  11  12  13  

num_page = 14
max_pages = 10
middle = 5   
currentpage
'''

def custom_paginator(current_page, num_pages, max_page):

    middle = math.ceil(max_page / 2)
    # 先考虑特殊情况
    if num_pages <= max_page:
        start = 1
        end = num_pages
    elif current_page <= middle:
        start = 1
        end = max_page
    elif middle < current_page < num_pages - middle + 1:
        start = current_page - middle
        end = current_page + middle -1
    else:
        start = num_pages - max_page + 1
        end = num_pages
    return start, end
