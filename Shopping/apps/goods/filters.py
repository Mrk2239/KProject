# # -*- coding: utf-8 -*-
import django_filters
from django.db.models import Q

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''

    pricemin = django_filters.NumberFilter('shop_price',help_text='最低价格',lookup_expr='gte')
    pricemax = django_filters.NumberFilter('shop_price',help_text='最高价格',lookup_expr='lte')
    #模糊查询,icontains忽略大小写
    #name = django_filters.CharFilter('name',help_text='商品名',lookup_expr='icontains')

    top_category = django_filters.NumberFilter(method='top_category_filter')


    '''
    所有商品的外键对应的都是二级分类,三级分类没有商品,而一级分类包含二级,三级分类
    '''
    # 导航实现过滤
    def top_category_filter(self,queryset,name,value):
        # 跨表查询__属性 双下划线,外键关系,value=pk   parent_category
        #return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

        # 此处category_id为二级类目id,category__parent_category_id=value为一级类目id
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value))
        # post.tags__id=pk, post.objects.filter(tags__id=pk)


    class Meta:
        model = Goods
        fields = ['pricemin','pricemax','is_hot','is_new']

