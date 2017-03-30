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
from lectur_app.views import Home, Register,RegisterProfile, UpdateProfile , Prueba, Comunidades, VistaComunidad, Explora, Destacados, Inicio_sesion, Perfil, VistaForo, VistaCategoriaForo, VistaTemaForo, CrearComunidad, CrearTaller, RegistrarEspacio, VistaComentario, CrearTema, Vistajax;

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

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
    url(r'^comunidades/(?P<comunidad>[-_\w]+)/(?P<tipo>[-_\w]+)/$', VistaComunidad.as_view(), name='comunidad_dos'),
    url(r'^explora/$', Explora.as_view(), name='explora_comunidades'),
    url(r'^destacados/$', Destacados.as_view(), name='destacados'),
    url(r'^inicia_sesion/$', Inicio_sesion.as_view(), name='inicia_sesion'),
    url(r'^cerrar_sesion/$', views.cerrar_sesion, name='cerrar_sesion'),
    url(r'^perfil/(?P<nombre>[-_\w]+)/$', Perfil.as_view(), name='vista_perfil'),
    url(r'^foro/(?P<foro>[-_\w]+)/$', VistaForo.as_view(), name='foro'),
    url(r'^foro/(?P<foro>[-_\w]+)/(?P<categoria>[-_\w]+)/$', VistaCategoriaForo.as_view(), name='foro_categoria'),
    url(r'^foro/(?P<foro>[-_\w]+)/(?P<categoria>[-_\w]+)/(?P<tema>[-_\w]+)/$', VistaTemaForo.as_view(), name='foro_tema'),

    url(r'^crea/comunidad/$', CrearComunidad.as_view(), name='crear_comunidad'),
    url(r'^crea/taller/(?P<comunidad>[-_\w]+)/$', CrearTaller.as_view(), name='crear_taller'),
    url(r'^crea/tema/(?P<comunidad>[-_\w]+)/(?P<categoria>[-_\w]+)/$', CrearTema.as_view(), name='crear_tema'),#tema
    url(r'^crea/espacio/(?P<comunidad>[-_\w]+)/$', RegistrarEspacio.as_view(), name='crear_espacio'),
    url(r'^comentar/foro/(?P<username>[-_\w]+)/(?P<pk>[0-9]+)/$', login_required(views.register_comment), name='crear_comentario'),
    url(r'^vista-comentario/(?P<pk>[0-9]+)/$', VistaComentario.as_view(), name='ver_comentario'),
    url(r'^respuestajax/(?P<respuesta>[ -_\w]+)/$', Vistajax.as_view(), name='vista_ajax'),
    url(r'^registrar-usuario-comunidad/(?P<username>[-_\w]+)/(?P<comunidad>[-_\w]+)/$',  login_required(views.registrarUsuarioComunidad), name='registrar_usuario_comunidad'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
