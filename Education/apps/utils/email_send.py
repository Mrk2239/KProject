# encoding: utf-8

from random import Random

from celery.loaders import app

from  users.models import EmailVerifyRecord
# 导入Django自带的邮件模块
from django.core.mail import send_mail,EmailMessage
# 导入setting中发送邮件的配置
from Mxonline3.settings import EMAIL_FROM
# 发送html格式的邮件:
from django.template import loader

import json
import logging
import http.client

from urllib.error import URLError
from urllib.parse import urlencode

from celery.schedules import crontab
from celery.task import periodic_task

'''
# 生成随机字符串,生成随机验证码
import random
import string
ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
print(ran_str)
'''

# 生成随机字符串,生成随机验证码
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

#print(random_str())


# 发送注册邮件
def send_register_eamil(email, send_type):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容:
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "Mr.K的小站 注册激活链接"
        # email_body = "欢迎注册mtianyan的慕课小站:  请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)
                        # 模板字符串渲染                          #调用了这个路由,激活链接        active/(?P<active_code>.*)/
        email_body = loader.render_to_string(
                "email_register.html",  # 需要渲染的html模板
                {
                    "active_code": code  # 参数
                }
            )

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        # 如果发送成功
        if send_status:
                pass
    elif send_type == "forget":
        email_title = "Mr.K小站 找回密码链接"
        email_body = loader.render_to_string(
            "email_forget.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()

    elif send_type == "update_email":
        email_title = "Mr.K小站 修改邮箱验证码"
        email_body = loader.render_to_string(
            "email_update_email.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()




