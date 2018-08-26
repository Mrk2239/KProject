# -*- coding: utf-8 -*-
import scrapy


class MyrenrenSpider(scrapy.Spider):
    name = 'myrenren'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    def parse(self, response):
        pass
