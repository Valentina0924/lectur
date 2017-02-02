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
from lectur_app.views import Home, Register,RegisterProfile, UpdateProfile , Prueba;

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='index'),
    url(r'^registrate/$', Register.as_view(), name='registrar'),
    url(r'^register/perfil/$', RegisterProfile.as_view(), name='registrar_perfil'),
    url(r'^update/perfil/$', UpdateProfile.as_view(), name='actualizar_perfil'),

    url(r'^prueba/$', Prueba.as_view(), name='Prueba'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
