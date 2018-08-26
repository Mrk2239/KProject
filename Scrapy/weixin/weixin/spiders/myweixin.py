# -*- coding: utf-8 -*-
import scrapy
import logging
from weixin.items import WeixinItem
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y/%M%d %H:%M%S' #设置时间格式
logging.basicConfig(filename='wx1.log',filemode='a+',format=LOG_FORMAT,datefmt=DATE_FORMAT)
class MyweixinSpider(scrapy.Spider):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    name = 'myweixin'
    allowed_domains = ['weixin.sogou.com','mp.weixin.qq.com']
    start_urls = ["http://weixin.sogou.com/pcindex/pc/pc_0/1.html"]

    logging.info('开始爬虫')

    def parse(self, response):
        publicNumList = response.xpath('//div[@class="txt-box"]')


        logging.info('出错了啊')
        for p in publicNumList:
            purl = p.xpath('./h3/a/@href').extract()[0]
            #print(purl)
            yield scrapy.Request(purl, callback=self.get_weixin, headers=self.headers)

    def get_weixin(self, response):
        # print("*****************" * 30)
        weixin = response.xpath('//div[@class="profile_inner"]')
        #print(len(weixin))
        # for wx in weixin:
        # weixinName = weixin.xpath('./strong[@class="profile_nickname"]/text()').extract()[0]
        # # #
        # publicNum = weixin.xpath('.//span[@class="profile_meta_value"]/text()').extract()[0]

        for wx in weixin:
            #print(le)
            weixinName = wx.xpath('./strong[@class="profile_nickname"]/text()').extract()[0]

            publicNum = wx.xpath('.//span[@class="profile_meta_value"]/text()').extract()[0]

        # articleTitle = response.xpath('//*[@id="activity-name"]/text()').extract()[0].strip()
        #
        # timere = 'publish_time = \"(.*?)\".*'
        # html = response.body.decode('utf-8')
        # # 发布时间
        # postdate = re.findall(timere, html, re.M)[0]
        # # 二维码
        # qrcodere = 'window.sg_qr_code=\"(.*?)\";'
        # qrcode = "https://mp.weixin.qq.com" + re.findall(qrcodere, html)[0].replace('\\x26amp;', '&')

        item = WeixinItem()
        item['publicNum'] = publicNum
        item['weixinName'] = weixinName
        #
        return item