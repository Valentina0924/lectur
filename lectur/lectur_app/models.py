#encoding:utf-8
from __future__ import unicode_literals

import string
import random
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Genero(models.Model):
    titulo = models.CharField(max_length=128)
    slug = models.SlugField(max_length=100, unique=True)
    def __unicode__(self):
            return self.title


class Lector(models.Model):
    user = models.OneToOneField(User);
    codigo= models.CharField(max_length=128); #17010001 año(2 últimos dígitos) mes(2 dígitos) cifra(4 dígitos)
    facebook = models.URLField(blank=True);
    twitter = models.URLField(blank=True);
    descripcion = models.TextField(max_length=400);
    fecha_ingreso = models.DateField(auto_now_add=True);
    imagen = models.ImageField(upload_to='profile_images/');
    def __unicode__(self):
        return unicode(self.codigo+" "+self.user.username);

class Valoracion(models.Model):
    """docstring for Valoracion."""
    lector = models.ForeignKey(Lector);
    opinion = models.TextField(max_length=400, blank=True);
    calificacion = models.DecimalField(max_digits=3, decimal_places=1,default=0.0)
    def __unicode__(self):
        return unicode(self.codigo+" "+self.user.username);


class Taller(models.Model):
    organizador = models.ForeignKey(Lector);
    fecha = models.DateTimeField();
    descripcion = models.TextField(max_length=400);
    imagen = models.ImageField(upload_to='talleres_images/');
    nombre = models.CharField(max_length=100); # Nombre del taller
    slug = models.SlugField(max_length=100, unique=True) # Nombre del taller sin carácteres espeiales
    cupos = models.IntegerField(default=0)
    participantes = models.ManyToManyField(Lector, related_name='participantes_taller');
    def __unicode__(self):
        return unicode(self.nombre+" "+self.organizador.user.username);

class Libro(models.Model):
    """docstring for Libro."""
    titulo = models.CharField(max_length=128);
    autor = models.CharField(max_length=128);
    portada = models.ImageField(upload_to='libros_images/');
    descripcion = models.TextField(max_length=400);
    generos = models.ManyToManyField(Genero, related_name='generos_libro');
    likes = models.ManyToManyField(User, related_name='likes_libro');
    valoraciones= models.ManyToManyField(Valoracion, related_name='valoraciones_libro');
    url = models.URLField(blank=True, null=True);
    def __unicode__(self):
        return unicode(self.titulo+" "+self.autor);

class Trabajo_Escrito(models.Model):
    """docstring for Libro."""
    titulo = models.CharField(max_length=128);
    autor = models.ForeignKey(Lector);
    descripcion = models.TextField(max_length=400);
    texto = models.TextField();
    generos = models.ManyToManyField(Genero, related_name='generos_escrito');
    likes = models.ManyToManyField(User, related_name='likes_escrito');
    valoraciones= models.ManyToManyField(Valoracion, related_name='valoraciones_escrito');
    isActive = models.BooleanField(default=True); # el texto se ha eliminado
    isPublic = models.BooleanField(default=True); # el texto es publico
    def __unicode__(self):
        return unicode(self.titulo+" "+self.autor.user.username);

class Espacio(models.Model):
    tipo = models.IntegerField(default = 1); # 0:Biblioteca 1:sala, 2: casa, 3: parque, 4:cafeteria
    direccion = models.CharField(max_length=40);
    latitud = models.DecimalField(max_digits=20, decimal_places=10,default=0.0);
    longitud = models.DecimalField(max_digits=20, decimal_places=10,default=0.0);
    nombre = models.CharField(max_length=20);
    descripcion = models.CharField(max_length=300);
    def __unicode__(self):
        return unicode(self.tipo+" "+self.nombre +" "+self.direccion);

class Evento(models.Model):
    dias = models.CharField(max_length=22); # "LU MA MI JU VI SA DO"
    hora_inicio = models.TimeField();
    hora_fin = models.TimeField();
    nombre = models.CharField(max_length=20);
    descripcion = models.CharField(max_length=200);
    tipo_repeticion = models.IntegerField(default=1); # 0:diario, 1:semanal, 2:mesual, 3:anual
    def __unicode__(self):
        return unicode(self.nombre+" "+self.dias);

class Info_Libro(models.Model):
    libro = models.ForeignKey(Libro);
    cantidad_total = models.IntegerField(default = 1);
    cantidad_disponible = models.IntegerField(default = 1);
    lectuales = models.ManyToManyField(Lector, related_name = 'lectores_actuales');
    def __unicode__(self):
        return unicode(self.libro);

class Biblioteca(models.Model):
    nombre = models.CharField(max_length=20);
    ubicacion = models.ForeignKey(Espacio);
    programacion = models.ManyToManyField(Evento, related_name = 'programacion_biblioteca');
    administradores = models.ManyToManyField(Lector, related_name = 'administradores_biblioteca');
    libros = models.ManyToManyField(Info_Libro, related_name = 'libros_biblioteca');
    espacios = models.ManyToManyField(Espacio, related_name = 'espacios_bibliotecas');
    def __unicode__(self):
        return unicode(self.nombre);

class Comunidad(models.Model):
    administradores = models.ManyToManyField(Lector, related_name = 'administradores_comunidad');
    participantes = models.ManyToManyField(Lector, related_name = 'participantes_comunidad');
    nombre = models.CharField(max_length=20);
    lugares_encuentro = models.ManyToManyField(Espacio, related_name = 'lugares_encuentro');
    libros = models.ManyToManyField(Info_Libro, related_name = 'libros_comunidad');
    bibliotecas_amigas = models.ManyToManyField(Biblioteca, related_name = 'biblioteca_amiga');
    talleres = models.ManyToManyField(Taller, related_name = 'talleres_comunidad');
    def __unicode__(self):
        return unicode(self.nombre);
