# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"



class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    '''
    外键关系,一级类目下的二级类目,由于定义了related_name=sub_cat,
    所以 CategorySerializer.CategorySerializer2_set.all()
    可写成CategorySerializer.sub_cat,外键定在多的一头
    '''
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )

class GoodsSerializer(serializers.ModelSerializer):
    #外键关系
    category = CategorySerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = '__all__'

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BrandsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'

class CategoryIndexSerializer(serializers.ModelSerializer):
    # 品牌名
    brands = BrandsSerializer(many=True)
    # 类目商品
    goods = serializers.SerializerMethodField()
    # 全部类目
    sub_cat = CategorySerializer2(many=True)
    # 广告品牌商品
    ad_goods = serializers.SerializerMethodField()

    # 类目下商品列表
    # 重写ListModelMixin下的拿到goods,嵌套serializer
    '''
    因为商品类别对应一级二级三级类目,应全部包括
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)
    '''
    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id)
                                         | Q(category__parent_category__parent_category_id=obj.id))
        '''
        context={'request':self.context['request'] 知识点,嵌套序列加上它可显示商品详情
        '''
        goods_serializer = GoodsSerializer(all_goods,many=True,context={'request':self.context['request']})

        return goods_serializer.data

    # 返回json数据
    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = '__all__'