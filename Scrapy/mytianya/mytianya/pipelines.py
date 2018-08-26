# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#管道,可去 重
class MytianyaPipeline(object):

    # #构造函数
    # def __init__(self):
    #     pass
    #
    # #打开爬虫时调用,调用一次
    # def open_spider(self,spider):
    #     self.f = open('tianya.txt','a+',encoding='utf-8')
    #     pass

    #写入
    def process_item(self, item, spider):
        # self.f.write(str(item['story']) + '\n')
        # self.f.flush()

        return item

    # 关闭爬虫时，调用一次
    # def close_spider(self,spider):
    #     self.f.close()
    #     pass

    # def __del__(self):
    #     #析构函数
    #     pass