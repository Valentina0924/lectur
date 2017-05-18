#encoding:utf-8
from __future__ import unicode_literals

import string
import random
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Foto(models.Model):
    titulo = models.CharField(max_length=50, default='Sin título')
    foto = models.ImageField(upload_to='fotos/')
    fecha_publicacion = models.DateField(auto_now_add=True)
    def __str__(self):
            return str(self.titulo)

class Notificacion(models.Model):
    imagen = models.ImageField(upload_to = 'notificaciones_images/');
    contenido = models.CharField(max_length=200);
    estado = models.IntegerField(default=1);
    usuario = models.ForeignKey(User);
    def __str__(self):
            return str(self.usuario)

class Felicitacion(models.Model):
    imagen = models.ImageField(upload_to = 'felicitaciones_images/');
    contenido = models.CharField(max_length=200);
    estado = models.IntegerField(default=1);
    usuario = models.ForeignKey(User);
    def __str__(self):
            return str(self.usuario)

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
    def __str__(self):
        return str(self.codigo+" "+self.user.username);

class Valoracion(models.Model):
    """docstring for Valoracion."""
    lector = models.ForeignKey(Lector);
    opinion = models.TextField(max_length=400, blank=True);
    calificacion = models.DecimalField(max_digits=3, decimal_places=1,default=0.0)
    def __unicode__(self):
        return unicode(self.codigo+" "+self.user.username);

class Espacio(models.Model):
    tipo = models.IntegerField(default = 1); # 0:Biblioteca 1:sala, 2: casa, 3: parque, 4:cafeteria, 5:otro
    direccion = models.CharField(max_length=40);
    latitud = models.DecimalField(max_digits=40, decimal_places=30,default=0.0);
    longitud = models.DecimalField(max_digits=40, decimal_places=30,default=0.0);
    nombre = models.CharField(max_length=20);
    descripcion = models.CharField(max_length=300);
    def __unicode__(self):
        return unicode(self.tipo+" "+self.nombre +" "+self.direccion);

class Taller(models.Model):
    organizador = models.ForeignKey(Lector);
    fecha = models.DateTimeField();
    descripcion = models.TextField(max_length=400);
    imagen = models.ImageField(upload_to='talleres_images/');
    nombre = models.CharField(max_length=100); # Nombre del taller
    slug = models.SlugField(max_length=100, unique=True) # Nombre del taller sin carácteres espeiales
    cupos = models.IntegerField(default=0)
    participantes = models.ManyToManyField(Lector, related_name='participantes_taller');
    ubicacion = models.ForeignKey(Espacio, null=True);

    def __str__(self):
        return str(self.nombre+" "+self.organizador.user.username);



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



class Evento(models.Model):
    dias = models.CharField(max_length=22); # "LU MA MI JU VI SA DO"
    hora_inicio = models.TimeField();
    hora_fin = models.TimeField();
    nombre = models.CharField(max_length=20);
    descripcion = models.CharField(max_length=200);
    tipo_repeticion = models.IntegerField(default=1); # 0:diario, 1:semanal, 2:mesual, 3:anual
    def __unicode__(self):
        return unicode(self.nombre+" "+self.dias);

class Respuesta(models.Model):
    perfil = models.ForeignKey(Lector);
    mensaje = models.CharField(max_length=200);
    fecha =  models.DateTimeField(auto_now_add=True);
    tipo_respuesta = models.IntegerField(default=-1); #menor a 0 dirigido al foro, mayor a 0 dirigido a otra respuesta
    def __str__(self):
        return str(self.perfil);

class Tema(models.Model):
    titulo = models.CharField(max_length=50,null=True);
    mensaje = models.CharField(max_length=400,null=True);
    autor =  models.ForeignKey(Lector);
    fecha_publicacion =  models.DateTimeField(auto_now_add=True);
    respuesta = models.ManyToManyField(Respuesta, related_name = 'respuesta_tema',blank=True);
    valoracion = models.ManyToManyField(Valoracion, related_name = 'valoracion_tema',blank=True);
    slug = models.SlugField(max_length=20, null=True); #unique=True //slug de la comunidad ala que pertenece el foro
    def __str__(self):
        return str(self.titulo);

class Categoria(models.Model):
    titulo = models.CharField(max_length=50);
    tema = models.ManyToManyField(Tema, related_name='tema_foro',blank=True);
    descripcion = models.CharField(max_length=200);
    slug = models.SlugField(max_length=50, null=True); #unique=True //slug de la comunidad ala que pertenece el foro
    tipo = models.IntegerField(default=0); #0=discusion, 1=creacion, 2=recomendacion
    def __str__(self):
        return str(self.titulo+" ("+self.slug+") "+self.descripcion);

class Foro(models.Model):
    categoria = models.ManyToManyField(Categoria, related_name='categoria_foro',blank=True);
    titulo = models.CharField(max_length=50);
    contenido = models.CharField(max_length=200);
    slug = models.SlugField(max_length=20, null=True); #unique=True //slug de la comunidad ala que pertenece el foro
    def __str__(self):
        return str(self.titulo);

class Comunidad(models.Model):
    administradores = models.ManyToManyField(Lector, related_name = 'administradores_comunidad',blank=True);
    participantes = models.ManyToManyField(Lector, related_name = 'participantes_comunidad',blank=True);
    nombre = models.CharField(max_length=20, unique=True);
    slug = models.SlugField(max_length=20, unique=True);
    lugares_encuentro = models.ManyToManyField(Espacio, related_name = 'lugares_encuentro',blank=True);
    #libros = models.ManyToManyField(Info_Libro, related_name = 'libros_comunidad');
    #bibliotecas_amigas = models.ManyToManyField(Biblioteca, related_name = 'biblioteca_amiga');
    talleres = models.ManyToManyField(Taller, related_name = 'talleres_comunidad',blank=True);
    album_fotos = models.ManyToManyField(Foto, related_name = 'fotos_comunidad',blank=True);
    descripcion = models.CharField(max_length=200);
    imagen = models.ImageField(upload_to='comunidades_images/', null=True);
    def __str__(self):
        return self.nombre;

class Reto(models.Model):
    titulo = models.CharField(max_length=30);
    slug = models.SlugField(max_length=20, unique=True);
    descripcion = models.CharField(max_length=200);
    nivel = models.IntegerField(default=0);
    def __str__(self):
        return str(self.titulo);

class Premio(models.Model):
    reto = models.ForeignKey(Reto);
    titulo = models.CharField(max_length=30);
    lista_ganadores = models.ManyToManyField(Lector, related_name ='ganadores_premio', blank = True);
    imagen = models.ImageField(upload_to='premio_images/');
    cantidad_minima = models.IntegerField(default=1);
    def __str__(self):
        return str(self.titulo+" ("+str(self.reto)+")");

class Genero_literario(models.Model):
    nombre = models.CharField(max_length=50);
    slug  = models.SlugField(max_length=50, unique=True);
    descripcion = models.CharField(max_length=250);
    comunidades = models.ManyToManyField(Comunidad, related_name='genero_comunidades', blank=True);
    temas = models.ManyToManyField(Tema, related_name='genero_tema_foro', blank=True);
