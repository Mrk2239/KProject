#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: InsertMysql.py
@time: 2018/7/12 0012 下午 10:42

'''
import json

import pymysql
import redis

mysqlconn = pymysql.connect(host='127.0.0.1',user='root',password='839916251',database='baike',port=3306,charset='utf8')

redisconn = redis.Redis(host='127.0.0.1',port=6379,db=0,password='839916251')


#print(mysqlconn,redisconn)

#游标
mysqlCur = mysqlconn.cursor()

#一直进行读写,直到弹空为止
while True:
    #从redis读取数据
    # FIFO从头弹,队列模式

    #"myBaikecrawler_redis:items"为redis的键
    clo,data = redisconn.blpop("myBaikecrawler_redis:items")
    #clo为redis的row行号,data为redis的value值(两个都是值)

    #为json数据unicode编码,需要转python数据(转为字典)
    item = json.loads(data)
    clos,value=zip(*item.items())
    sql = "INSERT INTO `%s` (%s) VALUES (%s)" % ('baidu',
                                                ','.join(clos),
                                                ','.join(['%s'] * len(value)))



    mysqlCur.execute(sql,value)
    mysqlconn.commit()

mysqlCur.close()
mysqlconn.close()
redisconn.close()
