from django import template
from django.contrib.contenttypes.models import ContentType
from lectur_app.models import Notificacion, Felicitacion
register = template.Library()


@register.filter(name='get_notificaciones')
def get_notificaciones (user):
    notificaciones=False;
    if user.is_authenticated:
        notificaciones=Notificacion.objects.filter(usuario=user).filter(estado__gt=0).order_by("-pk");
    return notificaciones;

@register.filter(name='get_felicitacion')
def get_felicitacion (user):
    felicitacion=False;
    if user.is_authenticated:
        felicitaciones=Felicitacion.objects.filter(usuario=user).filter(estado__gt=0);
        if felicitaciones:
            felicitacion=felicitaciones[0];
            felicitacion.estado=0;
            felicitacion.save();
    return felicitacion;
