"""lectur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,  url

from django.conf import settings
from django.contrib import admin
from lectur_app import views;
from lectur_app.views import Home, Register,RegisterProfile, UpdateProfile , Prueba, Comunidades, VistaComunidad, Explora, Destacados, Inicio_sesion, Perfil;

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='index'),
    url(r'^registrate/$', Register.as_view(), name='registrar'),
    url(r'^register/perfil/$', RegisterProfile.as_view(), name='registrar_perfil'),
    url(r'^update/perfil/$', UpdateProfile.as_view(), name='actualizar_perfil'),

    url(r'^prueba/$', Prueba.as_view(), name='Prueba'),
    url(r'^comunidades/$', Comunidades.as_view(), name='todas_comunidades'),
    url(r'^comunidades/(?P<comunidad>[-_\w]+)/$', VistaComunidad.as_view(), name='comunidad'),
    url(r'^explora/$', Explora.as_view(), name='explora_comunidades'),
    url(r'^destacados/$', Destacados.as_view(), name='destacados'),
    url(r'^inicia_sesion/$', Inicio_sesion.as_view(), name='inicia_sesion'),
    url(r'^cerrar_sesion/$', views.cerrar_sesion, name='cerrar_sesion'),
    url(r'^perfil/(?P<nombre>[-_\w]+)$', Perfil.as_view(), name='vista_perfil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
