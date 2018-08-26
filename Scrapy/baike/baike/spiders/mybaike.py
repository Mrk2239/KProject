# -*- coding: utf-8 -*-
import scrapy

from baike.items import BaikeItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MybaikeSpider(CrawlSpider):
    name = 'mybaike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/Python/407313']
    rules = [Rule(LinkExtractor(allow=('item/(.*?)')),callback='get_parse',follow=True)]
    def get_parse(self, response):
        # 百科关键字
        kw = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0]

        contentList = response.xpath('//div[@class="lemma-summary"]//text()')

        content = ''

        item = BaikeItem()

        for c in contentList:
            content += c.extract().strip().replace('\n', '')

        item['kw'] = kw
        item['content'] = content

        yield item
