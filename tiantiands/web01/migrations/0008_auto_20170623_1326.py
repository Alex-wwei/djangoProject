# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 05:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0007_product_icon_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderNumber',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='classification',
            field=models.IntegerField(),
        ),
    ]