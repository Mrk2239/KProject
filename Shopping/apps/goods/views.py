from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, HotSearchWords, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializers, \
    CategoryIndexSerializer


#分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 20

    page_size_query_param = 'page_size'
    page_query_param = 'page'


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
      商品列表页, 分页， 搜索， 过滤， 排序
    """
    # 限制游客 和 登录后的访问频率
    throttle_classes = (UserRateThrottle,AnonRateThrottle,)


    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    '''
    '^'开始 - 搜索。
    '='完全匹配。
    '@'全文搜索。（目前只支持Django的MySQL后端。）
    '$'正则表达式搜索。
    '''
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')


    """
    Retrieve a model instance.商品的点击数
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    '''
    商品一级,二级,三级分类,将全部类目嵌套形式显示出来,导航栏位置
        """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    '''

    # 二级三级类目嵌套在一级类目下显示
    queryset = GoodsCategory.objects.filter(category_type=1)

    serializer_class = CategorySerializer

class HotSerarchsViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取热搜关键词列表
    '''
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页轮播大图列表
    '''
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = BannerSerializers

class CategoryIndexViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页商品类别广告数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=['生鲜食品','酒水饮料','蔬菜水果'])
    serializer_class = CategoryIndexSerializer