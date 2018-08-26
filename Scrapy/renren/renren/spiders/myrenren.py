# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class MyrenrenSpider(CrawlSpider):
    name = 'myrenren'
    allowed_domains = ['renren.com']
    start_urls = ["http://www.renren.com/353111356/profile"]
    rules = [Rule(LinkExtractor(allow="(\d+)/profile"),callback='get_parse',follow=True)]

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }
    ## 爬虫开启时调用的第一个方法，只调用一次
    def start_requests(self):
        indexurl = "http://www.renren.com/"
        #获取登录前令牌
        yield scrapy.FormRequest(url=indexurl,
                                 meta={'cookiejar':1},#开启cookie记录
                                 callback=self.post_login

                                 #formdata={'email':'15083972239','password':'839916251'},
                                )

    #登录
    def post_login(self,response):
        # 从响应里面获取认证牌
        yield scrapy.FormRequest.from_response(response,
                                               url='http://www.renren.com/PLogin.do',
                                               meta={'cookiejar':response.meta['cookiejar']},
                                               formdata={'email': '15083972239', 'password': '839916251'},
                                               headers=self.headers,
                                               callback = self.after_login)

    #登录后
    def after_login(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url,meta={'cookiejar':response.meta['cookiejar']})

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                #更新cookie追踪
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])

                yield rule.process_request(r)


    def get_parse(self, response):
        print("******" * 30)
        print(response.body.decode('utf-8'))
        pass
