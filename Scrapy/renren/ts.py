#!/usr/bin/env python
# encoding: utf-8
'''
@author: kdb

@file: ts.py
@time: 2018/7/14 0014 上午 11:18

'''
cookie = "pgv_pvid=676298950; pgv_pvi=4321205248; RK=WLh0PPjUSz; ptcz=27c4bc909df38b9f9f5417176f300d5bb4e1a9596212c8ed0dbed8d2c683e4f5; _qpsvr_localtk=0.9056312749352518; ptisp=ctc; pgv_si=s4480360448; pgv_info=ssid=s7393639456; ptui_loginuin=1027141731; pt2gguin=o1027141731; uin=o1027141731; skey=@vXvkbrMpy; p_uin=o1027141731; pt4_token=JMMbdTtjwocIBLwiL1wHeW0CRsxbFCMab3Zc8UGnxds_; p_skey=i4H*68EzUTqZQ4Q5ZLGqjsS3LoLpHF0XL9pnkJdskeQ_; fnc=2; Loading=Yes; welcomeflash=1027141731_56310; randomSeed=442400; x-stgw-ssl-info=dbccbe62d3c14e2576de1bfa92aa7e4d|0.095|1531539504.831|1||||||q39|0"

cookieList = cookie.split(';')

cookieDict = {}
for cookie in cookieList:
    name = cookie.split('=',maxsplit=1)[0].strip()
    value = cookie.split('=',maxsplit=1)[1].strip()
    cookieDict[name] = value

print(cookieDict)