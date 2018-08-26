from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider

from example.items import BaikeItem


class MyBaikeCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'mybaikecrawler_redis'
    redis_key = 'mybaikecrawler:start_urls'
    #https://baike.baidu.com/item/Python/407313
    rules = (
        # follow all links
        Rule(LinkExtractor(allow=('item/(.*)')), callback="get_parse", follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('baidu.com', 'baike.baidu.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(MyBaikeCrawler, self).__init__(*args, **kwargs)

    def get_parse(self, response):
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