# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import timedelta
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()
# 自定义Serializer,因为不需要code字段在此,此处只验证手机号码,用于发送手机短信息验证码,验证码在view中产生
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('该用户已注册')
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('我认为你是乱输的号码')

        # 验证码发送频率,一分钟只能发送一条
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():

            raise serializers.ValidationError('距离上一次发送未超过60s,短信要钱的')

        #返回手机号码(类似于ModelFrom,post提交数据给后台)
        return mobile

#自定义 此处验证 发送的验证码 和 注册账号时验证
class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,label='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    # 注册时的用户名,不能为空,UniqueValidator唯一性
    username = serializers.CharField(label='用户名',help_text='用户名',required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    #style={'input':'password'}用于输入密码时不明文显示
    # write_only=True 为向后台提交数据后不返回
    password = serializers.CharField(
            style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
        )



    '''
    signals.py 此处给密码进行加密,用信号机制更加优雅,对于model里的,信号机制 会自动自己调用
    
    '''
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user


    def validate_code(self, code):
        '''
        用于检验 验证码
        :param code:
        :return:
        '''
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        #找到注册时该用户所对应的code ,此处username=mobile,都可用于注册验证

        # 未经验证之前的数据,form的label字段用户名  input name="username"
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        # 逆序,意味着找到最新的那条验证码,可能用户会连接点击发送几条验证码,
        #此时最后一条才有用
        if verify_records:
            last_record = verify_records[0]
            #设置验证码5分钟过期
            print(type(code),code)
            print(type(last_record),last_record)
            print(str(last_record) == str(code))
            if last_record.add_time  < datetime.now() - timedelta(hours=0, minutes=5, seconds=0):
                raise serializers.ValidationError("验证码过期")
            # 和发送成功后保存在数据库中的验证码对比,需要一致
            if str(last_record) != code:
                raise serializers.ValidationError('验证码就四位数你还输错')
        else:
            raise serializers.ValidationError("验证码错误")

    # 清除code属性,不需要保存到数据库中
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return  attrs

    # serializers上面写的字段会覆盖Meta里fields的
    class Meta:
        model = User
        fields = ('username','code','mobile','password')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = ('id',"name", "gender", "birthday", "email", "mobile")

