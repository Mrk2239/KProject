# -*- coding: utf-8 -*-
import time

from rest_framework import serializers

from MxShop.settings import private_key_path, ali_pub_key_path
from utils.alipay import AliPay
from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods


class UserShoppingCartDeatilSerializer(serializers.ModelSerializer):
    # 外键 ,一个购物车商品记录只能对应一件商品
    goods = GoodsSerializer(read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")

class UserShoppingCartSerializer(serializers.Serializer):
    """
    因为购物车增加同一商品时,联合唯一组建的存在,会报错,不能继承serializers.ModelSerializer
    所以继承serializers.Serializer,需要重写create和update
    购物车商品记录的增删改查
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 加入购物车商品数量最小值为1
    nums = serializers.IntegerField(required=True, label='商品数量', min_value=1,
                                    error_messages={'required': '请选择商品数量', 'min_value': '加入购物车商品数量最小值为1'})

    # 外键 因为没有继承serializers.ModelSerializer
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # validated_data中数据已经经过验证
    def create(self, validated_data):
        # 有点类似于modelform
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        # 查询购物车记录,是否存在这一商品信息,有则加nums数量和save,无则差创建,把该商品加入购物车
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    # 商品数量的更新,instance实例
    def update(self,instance,validated_data):

        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    # odergood 的 外键 goods，非多的那一头
    goods = GoodsSerializer()
    class Meta:
        model = OrderGoods
        fields = '__all__'

#订单详情页
class OrderDetailSerializer(serializers.ModelSerializer):
    # 订单的商品详情
    goods = OrderGoodsSerializer(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016091700529061",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        # 订单的相关信息
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"

# 用户订单页
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    # 生成随机订单号
    def generate_order_sn(self):
        # 当前时间+userid+随机数
        import random
        #从上下文中获取user=self.context['request'].user
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                       userid=self.context['request'].user.id,
                                                       ranstr=random.randint(10,100))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'