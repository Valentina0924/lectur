# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectur_app', '0012_auto_20170323_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='foro',
            name='tipo',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='administradores',
            field=models.ManyToManyField(blank=True, related_name='administradores_comunidad', to='lectur_app.Lector'),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='participantes_comunidad', to='lectur_app.Lector'),
        ),
    ]