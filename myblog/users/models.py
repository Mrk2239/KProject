from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(verbose_name="昵称",max_length=50)
    headshot = models.ImageField(verbose_name='头像',upload_to='avatar/%Y/%m/%d',default='default.jpg')
    signature = models.CharField(verbose_name='个性签名',max_length=128,default='this guy is too lazy to leave anything here!')

    class Meat(AbstractUser.Meta):
        pass