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
    name = 'myqq'
    allowed_domains = ['user.qzone.qq.com']

    start_urls = ['https://user.qzone.qq.com/1027141731']

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    #cookie = {'pgv_pvid': '676298950', 'pgv_pvi': '4321205248', 'RK': 'WLh0PPjUSz', 'ptcz': '27c4bc909df38b9f9f5417176f300d5bb4e1a9596212c8ed0dbed8d2c683e4f5', '_qpsvr_localtk': '0.9056312749352518', 'ptisp': 'ctc', 'pgv_si': 's4480360448', 'pgv_info': 'ssid=s7393639456', 'ptui_loginuin': '1027141731', 'pt2gguin': 'o1027141731', 'uin': 'o1027141731', 'skey': '@vXvkbrMpy', 'p_uin': 'o1027141731', 'pt4_token': 'JMMbdTtjwocIBLwiL1wHeW0CRsxbFCMab3Zc8UGnxds_', 'p_skey': 'i4H*68EzUTqZQ4Q5ZLGqjsS3LoLpHF0XL9pnkJdskeQ_', 'fnc': '2', 'Loading': 'Yes', 'welcomeflash': '1027141731_56310', 'randomSeed': '442400', 'x-stgw-ssl-info': 'dbccbe62d3c14e2576de1bfa92aa7e4d|0.095|1531539504.831|1||||||q39|0'}


    ## 爬虫开启时调用的第一个方法，只调用一次
    # def start_requests(self):
    #
    #
    #     yield scrapy.Request(url=self.start_urls[0],
    #                              cookies=self.cookie,
    #                              callback=self.parse,
    #                              headers = self.headers,
    #                              #formdata={'email':'15083972239','password':'839916251'},
    #                             )


    def parse(self, response):
        print("******" * 30)
        print(response.body.decode('utf-8'))
        pass
