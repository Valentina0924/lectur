
from django import template
from django.contrib.contenttypes.models import ContentType
from lectur_app.models import Respuesta
register = template.Library()

@register.filter(name='get_respuestas_foro')
def get_respuestas_foro (pk):
    respuestas=Respuesta.objects.filter(tipo_respuesta=pk);
    return respuestas;


@register.filter(name='cantidad_temas_categoria')
def cantidad_temas_categoria(cate):
    cant = len(cate.tema.all()) ;
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
