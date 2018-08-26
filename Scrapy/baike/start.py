#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: start.py
@time: 2018/7/10 0010 下午 5:48

'''

import scrapy.cmdline

def main():
    scrapy.cmdline.execute(['scrapy','crawl','mybaike'])

if __name__ == '__main__':
    main()