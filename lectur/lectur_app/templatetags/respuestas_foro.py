
from django import template
from django.contrib.contenttypes.models import ContentType
from lectur_app.models import Respuesta, Categoria, Tema, Foro, Comunidad
register = template.Library()

@register.filter(name='get_respuestas_foro')
def get_respuestas_foro (pk):
    respuestas=Respuesta.objects.filter(tipo_respuesta=pk);
    return respuestas;

@register.filter(name='cantidad_temas_categoria')
def cantidad_temas_categoria(cate):
    cant = len(cate.tema.all()) ;
    return cant;

@register.filter(name='get_categoria_tema')
def get_categoria_tema(tema):
    categorias = Categoria.objects.all();
    for cate in categorias:
        if tema in cate.tema.all():
            return cate;
    return False;

@register.filter(name='get_foro_categoria')
def get_foro_categoria(categoria):
    foros = Foro.objects.all();
    for foro in foros:
        if categoria in foro.categoria.all():
            return foro;
    return False;

@register.filter(name='get_comunidad_foro')
def get_comunidad_foro(foro):
    comunidad=False;
    if foro and foro.slug!="tulia":
        comunidad = Comunidad.objects.get(slug=foro.slug);
    return comunidad;

@register.filter(name='cantidad_respuestas_tema')
def cantidad_respuestas_tema(tema):
    cant = len(tema.respuesta.all()) ;
    return cant;

@register.filter(name='get_imagen_categoria')
def get_imagen_categoria(tipo):
    img="imagenes/icono_one.png";
    if tipo==0:
        img="imagenes/icono_one.png";
    elif tipo==1:
        img="imagenes/icono_two.png";
    elif tipo==2:
        img="imagenes/icono_tree.png";
    return img;
