from django import template
from django.contrib.contenttypes.models import ContentType
from lectur_app.models import Notificacion
register = template.Library()


@register.filter(name='get_notificaciones')
def get_notificaciones (user):
    notificaciones=False;
    if user.is_authenticated:
        notificaciones=Notificacion.objects.filter(usuario=user).filter(estado__gt=0).order_by("-pk");
    return notificaciones;
