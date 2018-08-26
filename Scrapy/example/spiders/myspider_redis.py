from scrapy_redis.spiders import RedisSpider

from example.items import BaikeItem


class MyBaikeSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myBaikespider_redis'
    redis_key = 'myBaikespider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('baidu.com','baike.baidu.com')#允许爬取的域
        self.allowed_domains = filter(None, domain.split(','))
        super(MyBaikeSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 百科关键字
        kw = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0]

        # 关键字描述
        contentList = response.xpath('//div[@class="lemma-summary"]//text()')

        content = ""

        item = BaikeItem()

        for c in contentList:
            content += c.extract().strip().replace('\n', '')

        item['kw'] = kw
        item['content'] = content

        yield item