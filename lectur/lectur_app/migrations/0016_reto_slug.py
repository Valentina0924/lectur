# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectur_app', '0015_auto_20170330_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='reto',
            name='slug',
            field=models.SlugField(default='holi', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
