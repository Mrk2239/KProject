from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status, authentication, mixins, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from MxShop.settings import APIKEY
from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()
# Create your views here.

# 此处用于登录验证
class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    # 通过username和mobile找到user进行登录
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码,创建
    '''
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取手机号码
        mobile = serializer.validated_data['mobile']
        # 发送短信验证码
        yun_pian = YunPian(APIKEY) # 创建实例
        code = yun_pian.generate_code()
        sms_status = yun_pian.send_sms(code=code,mobile=mobile)

        # 云片 状态sms_status为0时发送成功
        # 此处判定短信是否发送成功!,并给前端返回相应的状态码

        if sms_status['code'] !=0:
            return Response({
                'mobile':sms_status['msg']
            },status=status.HTTP_400_BAD_REQUEST)

        else:
            # 验证码发送成功后就保存VerifyCode对象到数据库,注意此处应该发送成功后保存
            # 保存到的数据用于接下来的注册过程中对比认证
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()

            # 给前端返回数据和状态码
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    '''
    创建用户,注册过程
    获取用户详情页

    User一个资源,对应增删改查四个操作,通用这个UserViewset
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    # JWT ,jwt认证
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 如果获取个人详情或者注册等,序列化的不同
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer

        return UserDetailSerializer



    def get_permissions(self):
        """
        根据action,动态获取permissions
        """
        # 如果获取个人详情,需要登录验证
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []

        return []

    '''
    获取当前用户,API接口, GET user/pk ,因为返回的数据中并没有包含user.pk,
    所以重写get_object方法,接受pk这个参数,获取当前用户,retrieve
       def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    '''
    def get_object(self):
        return self.request.user


    # 创建用户
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #拿到user对象
        user=self.perform_create(serializer)

        #要返回的数据
        re_dict = serializer.data

        '''
        此处用于 注册成功后直接登录(看源码)
        
        payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        JWT post提交数据认证成功后会保存在cookie里,一般和user.name一起
        '''
        payload = jwt_payload_handler(user)
        # jwt会给我们 生成token 返回给前端,自定义 name 也一并返回给前端,然后保存在客户端浏览器中
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 返回user实例对象
    def perform_create(self, serializer):
        return serializer.save()
    '''
    Create a model instance.
    return serializer.save() 为 return user 
       #拿到user对象,为模板的实例对象,
        返回user对像给上文 user=self.perform_create(serializer)
    '''
