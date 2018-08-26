# -*- coding: utf-8 -*-

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav

'''
    # 收藏数量的增减
    def perform_create(self, serializer):
        instance=serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
        instance.delete()

'''

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):

    goods = instance.goods
    goods.fav_num += 1
    goods.save()


@receiver(post_delete,sender=UserFav)
def delete_userfav(sender,instance=None, created=False, **kwargs):

    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
