# -*- coding: utf-8 -*-
import re
import scrapy

#from tianya.items import TianyaItem
from mytianya.items import MytianyaItem


class TianyaSpider(scrapy.Spider):
    #爬虫名字
    name = 'tianya'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/post-140-393974-1.shtml']

    #爬虫逻辑
    def parse(self, response):

        #print(response.body.decode('utf-8'))

        #爬取页面邮箱
        emailre = '[a-z0-9_]+@[a-z0-9]+\.[a-z]{2,4}'
        emaillist = re.findall(emailre,response.body.decode('utf-8'),re.I)
        print(emaillist)

        # 实例一个存储对象
        #按字典格式读取
        item = MytianyaItem()
        # item['email'] = emaillist
        # return item

        #生成器
        for email in emaillist:
            item['email'] = email

            #生成一个
            yield item
