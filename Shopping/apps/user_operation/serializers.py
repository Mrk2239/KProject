# -*- coding: utf-8 -*-
import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from MxShop.settings import REGEX_MOBILE
from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('id','goods')


class UserFavSerializer(serializers.ModelSerializer):
    # 默认为当前登录用户下
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = UserFav
        # UniqueTogetherValidator 作用于多个字段上
        validators=[
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields = ('user','goods'),
                message='已经收藏'
            )
        ]


        fields = ('user','goods','id')

class UserLeavingMessageSerializer(serializers.ModelSerializer):
    # 默认为当前登录用户下
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")

class UserAddressSerializer(serializers.ModelSerializer):

    # 默认为当前登录用户下,把user序列化和反序列化,传参user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')

    # # 验证signer_mobile
    # signer_mobile = serializers.CharField(max_length=11, required=True)
    # def validate_signer_mobile(self, signer_mobile):
    #     if not re.match(REGEX_MOBILE, signer_mobile):
    #         raise serializers.ValidationError('我认为你是乱输的号码')

    class Meta:
        model = UserAddress
        fields = ('user','province','city','district','address','signer_name','signer_mobile','add_time','id')