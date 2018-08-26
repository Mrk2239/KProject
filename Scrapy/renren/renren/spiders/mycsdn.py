#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: mycsdn.py
@time: 2018/7/14 0014 下午 1:39

'''
#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: myQQ.py
@time: 2018/7/14 0014 上午 11:34

'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class MyqqSpider(scrapy.Spider):
    name = 'mycsdn'
    allowed_domains = ['csdn.net']

    start_urls = ['http://passport.csdn.net/account/login',
                  'https://my.csdn.net/my/account/changepwd']

    def __init__(self):
        super().__init__()

        driver = None   #实例selenium
        cookies = None  #用来保存cookie

    def parse(self, response):
        print(response.url)
        print("******" * 30)
        print(response.body.decode('utf-8'))
        pass
