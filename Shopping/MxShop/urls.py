"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.generic import TemplateView
from rest_framework.authtoken import views

import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet, HotSerarchsViewset, BannerViewset, CategoryIndexViewset
from trade.views import UserShoppingCartViewSet, OrderViewset, AlipayView

from user_operation.views import UserFavViewset, UserLeavingMessageViewset, UserAddressViewSet

from users.views import SmsCodeViewset, UserViewset
router = DefaultRouter()

#配置goods的url
router.register(r'goods',GoodsListViewSet,base_name='goods')
router.register(r'categorys',CategoryViewSet,base_name='categorys')

router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'shopcarts',UserShoppingCartViewSet,base_name='shopcarts')
router.register(r'users', UserViewset, base_name="users")
router.register(r'userfavs',UserFavViewset,base_name='userfavs')
router.register(r'messages',UserLeavingMessageViewset,base_name='messages')
router.register(r'address',UserAddressViewSet,base_name='address')
router.register(r'orders',OrderViewset,base_name='orders')
router.register(r'hotsearchs',HotSerarchsViewset,base_name='hotsearchs')
router.register(r'banners',BannerViewset,base_name='banners')
# 首页商品类别广告数据
router.register(r'indexgoods',CategoryIndexViewset,base_name='indexgoods')


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^',include(router.urls)),
    url(r'docs/', include_docs_urls(title="慕学生鲜")),

    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口,登录时使用
    url(r'^login/$', obtain_jwt_token),

    # 在django服务器上跑前端页面
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    # 支付接口
    url(r'^alipay/return/', AlipayView.as_view(), name="alipay"),

]
