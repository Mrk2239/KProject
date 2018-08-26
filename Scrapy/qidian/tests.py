#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: tests.py
@time: 2018/7/11 0011 上午 10:24

'''


def get_third(self, response):
    # 一章节P_list
    Third = (response.xpath("//div[@class='read-content j_readContent']/p"))
    # print(len(Third))
    # print(Third)

    # 全部章节内容
    story = ''
    for i in Third:
        s = (i.xpath('./text()').extract()[0])
        print(s)
        print('='*30)
        story = s + '\n'

        #
        # print('='*30)
        # print(story)

        item = QidianItem()
        item['story'] = story
        # return item
        yield item