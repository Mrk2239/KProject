# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def process_item(self, item, spider):
        # item["crawled"] = datetime.utcnow()
        # item["spider"] = spider.name

      #'mybaike:requests' 待请求的url,入队
      #'mybaike:dupefilter' 已经请求过的,记录url是否被爬取过,出队,实现去重
      #'mybaike:items' 爬取的字段


        return item
