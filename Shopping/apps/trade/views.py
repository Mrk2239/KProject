from datetime import datetime

from django.shortcuts import render, redirect
from MxShop.settings import private_key_path, ali_pub_key_path

# Create your views here.
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import UserShoppingCartSerializer, UserShoppingCartDeatilSerializer, OrderSerializer, \
    OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserShoppingCartViewSet(ModelViewSet):
    """
    购物车的商品记录的增删改查
    """
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """

    serializer_class = UserShoppingCartSerializer

    #lookup_field = 'goods_id'

    # 使用局部配置

    # 进行用户认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    # 进行用户权限设置
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserShoppingCartDeatilSerializer

        else:
            return UserShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


    '''
    根据购物车商品数量的变化 以及购物车记录的创建和删除 >> 对应的库存
    '''

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        nums = instance.nums
        goods.goods_num -= nums
        goods.save()

    def perform_destroy(self, instance):

        goods = instance.goods
        nums = instance.nums
        goods.goods_num += nums
        goods.save()
        instance.delete()

    # 购物车商品数量的变动update
    def perform_update(self, serializer):
        # 根据serializer拿到 instance 实例id,取到购物车变动之前的记录
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        # 记录中购物车的商品的数量

        existed_nums = existed_record.nums
        # 购物车商品数量的变动之后商品的数量
        saved_record=serializer.save()
        # 购物车商品前后数量之差
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewset(ModelViewSet):

    # 进行用户认证和权限设置
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer


    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        '''
        每个用户有多条购物车记录，每个购物车记录里面对应商品数量
        '''
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        # 订单_goods详情
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 订单创建后 ，删除购物车记录
            shop_cart.delete()
        return order



# 阿里支付
from rest_framework.views import APIView
from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response
class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回   支付完返回到 商城首页index
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091700529061",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url  通知url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091700529061",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    # 商品的销售量+
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")

