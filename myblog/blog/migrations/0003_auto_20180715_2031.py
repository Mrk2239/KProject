# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-15 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180707_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_time']},
        ),
    ]