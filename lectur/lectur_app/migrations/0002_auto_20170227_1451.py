# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lectur_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=22)),
                ('descripcion', models.CharField(max_length=52)),
            ],
        ),
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=22)),
                ('contenido', models.CharField(max_length=52)),
                ('categoria', models.ManyToManyField(related_name='categoria_foro', to='lectur_app.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Premio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('imagen', models.ImageField(upload_to='premio_images/')),
                ('lista_ganadores', models.ManyToManyField(related_name='ganadores_premio', to='lectur_app.Lector')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=22)),
                ('mensaje', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo_respuesta', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Reto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=200)),
                ('nivel', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectur_app.Lector')),
                ('respuesta', models.ManyToManyField(related_name='respuesta_tema', to='lectur_app.Respuesta')),
                ('valoracion', models.ManyToManyField(related_name='valoracion_tema', to='lectur_app.Valoracion')),
            ],
        ),
        migrations.RemoveField(
            model_name='biblioteca',
            name='administradores',
        ),
        migrations.RemoveField(
            model_name='biblioteca',
            name='espacios',
        ),
        migrations.RemoveField(
            model_name='biblioteca',
            name='libros',
        ),
        migrations.RemoveField(
            model_name='biblioteca',
            name='programacion',
        ),
        migrations.RemoveField(
            model_name='biblioteca',
            name='ubicacion',
        ),
        migrations.RemoveField(
            model_name='info_libro',
            name='lectuales',
        ),
        migrations.RemoveField(
            model_name='info_libro',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='generos',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='valoraciones',
        ),
        migrations.RemoveField(
            model_name='comunidad',
            name='bibliotecas_amigas',
        ),
        migrations.RemoveField(
            model_name='comunidad',
            name='libros',
        ),
        migrations.DeleteModel(
            name='Biblioteca',
        ),
        migrations.DeleteModel(
            name='Info_Libro',
        ),
        migrations.DeleteModel(
            name='Libro',
        ),
        migrations.AddField(
            model_name='premio',
            name='reto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectur_app.Reto'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='tema',
            field=models.ManyToManyField(related_name='tema_foro', to='lectur_app.Tema'),
        ),
    ]
