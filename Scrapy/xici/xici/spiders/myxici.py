# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider,Rule  #爬取规则
from scrapy.linkextractors import LinkExtractor #提取链接
import re

from xici.items import XiciItem


class MyxiciSpider(CrawlSpider):
    name = 'myxici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/wn/1']
    rules = (Rule(LinkExtractor(allow=("http://www.xicidaili.com/wn/(\d+)")), callback='get_parse', follow=True),)
    def get_parse(self, response):
        #print(response.text)
        ip_list = response.xpath('//table//tr[position()>1]')
        item = XiciItem()

        for xi in ip_list:
            ip = xi.xpath('./td[2]/text()').extract()[0]
            port = xi.xpath('./td[3]/text()').extract()[0]
            #print(ip,port)
        #

            item['ip'] = ip
            item['port'] = port

            yield item