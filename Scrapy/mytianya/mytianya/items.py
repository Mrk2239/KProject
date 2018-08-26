# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#自定义要爬取的字段
class MytianyaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    email = scrapy.Field()

    pass
