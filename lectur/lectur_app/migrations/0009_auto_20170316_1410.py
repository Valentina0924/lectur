# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectur_app', '0008_auto_20170316_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='tema',
            name='mensaje',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tema',
            name='titulo',
            field=models.CharField(max_length=22, null=True),
        ),
    ]
