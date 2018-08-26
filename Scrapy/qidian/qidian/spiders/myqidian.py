# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule  #爬取规则
from scrapy.linkextractors import LinkExtractor #提取链接

from qidian.items import QidianItem


class MyqidianSpider(CrawlSpider):
    name = 'myqidian'
    allowed_domains = ['qidian.com']
    #start_urls = ['https://www.qidian.com/free/all?chanId=21&action=1&orderId=&vip=hidden&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=1&page=1']
    start_urls = ['https://www.qidian.com/free/all?chanId=21&action=1&orderId=&page=2&vip=hidden&style=2&pageSize=20&siteid=1&pubflag=0&hiddenField=1']
    #https: // www.qidian.com / free / all?chanId = 21 & action = 1 & orderId = & vip = hidden & style = 2 & pageSize = 50 & siteid = 1 & pubflag = 0 & hiddenField = 1 & page = 2
    #rules = (Rule(LinkExtractor(allow=("https://www.qidian.com/free/all?chanId=21&action=1&orderId=&vip=hidden&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=1&page=(\d+)")), callback='get_parse', follow=True),)
    #rules = (Rule(LinkExtractor(allow=("http://www.xicidaili.com/nn/(\d+)")), callback='get_parse', follow=True),)
    #rules = (Rule(LinkExtractor(allow=("start=(\d+)#a")), callback='get_parse', follow=True),)
    rules = (Rule(LinkExtractor(allow=("&page=(\d+)&")), callback='get_parse', follow=True),)
    # + '#Catalog'
    def get_parse(self, response):
        FirstUrls = response.xpath('//*[@id="free-channel-wrap"]/div/div/div[2]/div[2]/div/table/tbody/tr/td[2]/a/@href')
        for FirstUrl in FirstUrls:
            #print(FirstUrl)
            FirstUrl = 'https:' + FirstUrl.extract() + '#Catalog'
            #print(FirstUrlz)
            request = scrapy.Request(url=FirstUrl,callback=self.get_second)

            yield request

    def get_second(self,response):
        SecondUrl = response.xpath("//div[@class='volume-wrap']/div[@class='volume']/ul/li/a/@href")
        for i in SecondUrl:
            #print('https:'+i.extract())
            url = 'https:'+i.extract()

            request = scrapy.Request(url=url, callback=self.get_third)
            yield request
        #print(SecondUrl)

    def get_third(self, response):
        # 一个章节P_list
        Third = (response.xpath("//div[@class='read-content j_readContent']//p"))
        # print(len(Third))
        # print(Third)

        # 一章节内容
        story = ''
        for i in Third:
            story += (i.xpath('./text()').extract()[0]).strip() + '\n'
        print(story)
            # print('=' * 30)
            # story = s + '\n'

            #
            # print('='*30)
            # print(story)

        item = QidianItem()
        item['story'] = story
            # return item
        yield item