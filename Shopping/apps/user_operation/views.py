from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, \
    UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):

    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    delete:
        取消收藏
    收藏列表,增加收藏,取消收藏,收藏商品详情
    '''
    #queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

    # 进行用户认证和权限设置
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)
    '''
    lookup_field - 应用于执行单个模型实例的对象查找的模型字段。默认为'pk'。请注意，使用超链接的API时，
    您需要确保双方的API意见和串行类设置查找字段，如果你需要使用一个自定义值。
    lookup_url_kwarg - 应该用于对象查找的URL关键字参数。URL conf应包含与此值对应的关键字参数。
    如果未设置，则默认使用相同的值lookup_field。
    '''
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 动态传递serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        else:
            return UserFavDetailSerializer

    # # 收藏数量的增减(采用信号机制)
    # def perform_create(self, serializer):
    #     instance=serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()
    #
    # def perform_destroy(self, instance):
    #     goods = instance.goods
    #     goods.fav_num -= 1
    #     goods.save()
    #     instance.delete()



class UserLeavingMessageViewset(ModelViewSet):
    '''
    用户留言
    增删改查
    '''

    serializer_class = UserLeavingMessageSerializer

    # 进行用户认证和权限设置
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class UserAddressViewSet(ModelViewSet):
    '''
    用户地址
    增删改查
    '''
    serializer_class = UserAddressSerializer

    # 进行用户认证和权限设置
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)