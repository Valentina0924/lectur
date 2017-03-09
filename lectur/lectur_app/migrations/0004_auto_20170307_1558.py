# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectur_app', '0003_comunidad_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='comunidad',
            name='descripcion',
            field=models.CharField(default='Somos unos peluches a los que nos gusta leer.', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='lugares_encuentro',
            field=models.ManyToManyField(blank=True, related_name='lugares_encuentro', to='lectur_app.Espacio'),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='talleres',
            field=models.ManyToManyField(blank=True, related_name='talleres_comunidad', to='lectur_app.Taller'),
        ),
    ]