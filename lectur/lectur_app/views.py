# -*- encoding: utf-8 -*-
from django.shortcuts import render
import datetime
from django.template.defaultfilters import slugify

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

from django.views.generic import View, FormView, UpdateView, CreateView, DetailView, ListView, TemplateView
from lectur_app.forms import UserForm, LectorForm;
from lectur_app.models import Lector

from django.conf import settings


# Create your views here.

# Create your views here.
class Home(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["aaa"]="Nadie";
        return context

class Register(CreateView):
	""" Vista de la página de formulario donde se registra un nuevo usuario """
	template_name = 'register.html'
	form_class = UserForm
	model = User

	def form_valid(self, form):
		user = form.save(commit=False)
		user.username = user.username.lower()
		user.set_password(user.password)
		user.save()
		p=form.data["password"]
		u= auth.authenticate(username=user.username, password=p)
		if u is not None and u.is_active:
			auth.login(request=self.request, user=u)
		return HttpResponseRedirect('/register/perfil/')


def get_codigo_nuevo_usuario():
    hoy = datetime.datetime.today();
    an=hoy.year-2000;
    mes=hoy.month;
    if(mes<10):
        cod=str(an)+"0"+str(mes);
    else:
        cod=str(an)+""+str(mes);
    cant=len(Lector.objects.filter(fecha_ingreso__year=hoy.year, fecha_ingreso__month=hoy.month));
    if cant < 10:
        cod=cod+"000";
    elif cant<100:
        cod=cod+"00";
    elif cant<1000:
        cod=cod+"0";

    cod=cod+str(cant);
    return cod;


class RegisterProfile(CreateView):
    """ Vista de la página de formulario donde se registra un nuevo usuario """
    template_name = 'register.html'
    form_class = LectorForm
    model = User

    def form_valid(self, form):
        lector = form.save(commit=False);
        lector.user = self.request.user;
        if not lector.codigo:
            lector.codigo=get_codigo_nuevo_usuario();
        lector.save();
        form.save_m2m();
        return HttpResponseRedirect('/prueba');

class UpdateProfile(UpdateView):
    """ Vista de la página de formulario donde se registra un nuevo usuario """
    template_name = 'register.html'
    form_class = LectorForm
    model = User
    state=False

    def get_state(self):
    	return state

    def get_object(self, queryset=None):
    	user = self.request.user;
    	obj = Lector.objects.get(user=user)
    	return obj

    def form_valid(self, form):
        lector = form.save();
        #dir='7perfil/'+lector.codigo
        return HttpResponseRedirect('/prueba');



class Prueba(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(Prueba, self).get_context_data(**kwargs)
        user= self.request.user;
        if user.is_authenticated():
            userprofile= Lector.objects.get(user=user);
            info= user.username +" | "+ userprofile.codigo +": "+ userprofile.descripcion;
            context["aaa"]=info;
            context["img"]=userprofile.imagen;
        return context
