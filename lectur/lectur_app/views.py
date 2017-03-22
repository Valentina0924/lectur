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
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


from django.views.generic import View, FormView, UpdateView, CreateView, DetailView, ListView, TemplateView
from lectur_app.forms import UserForm, LectorForm, UserLoginForm;
from lectur_app.models import Lector, Comunidad, Foro

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
    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context["seccion_header"]="Destacados";
        return context;
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



class Inicio_sesion(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = '/'


    redirect_field_name = REDIRECT_FIELD_NAME
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super(Inicio_sesion, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
        	self.request.session.delete_test_cookie()
        return super(Inicio_sesion, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.success_url
        return redirect_to

@login_required
def cerrar_sesion(request):
	"""
	Cierra la sesión activa.
	args:
		request.
	return:
		 HttpResponseRedirect: Redirecciona al iicio.
	"""
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect('/')


class Perfil(TemplateView):
    template_name = 'perfil.html'
    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        context["seccion_header"]="Perfil";
        nombreUsuario=self.kwargs["nombre"];
        usuario = User.objects.all().get(username=nombreUsuario);
        lec = Lector.objects.all().get(user=usuario);

        context["perfil"]=lec;

        comunidades= set([]);
        for com in Comunidad.objects.all():
            for adm in com.administradores.all():
                if adm==lec:
                    comunidades.add(com);
            for par in com.participantes.all():
                if par==lec:
                    comunidades.add(com);

        context["comunidades"] =comunidades;

        return context;

class Comunidades(TemplateView):
    template_name = 'explora_comunidades.html'
    def get_context_data(self, **kwargs):
        context = super(Comunidades, self).get_context_data(**kwargs)
        context["seccion_header"]="Comunidades";

        comunidades = Comunidad.objects.all();
        context["comunidades"]=comunidades;
        return context

class VistaComunidad(TemplateView):
    template_name = 'vista_comunidad.html'
    def get_context_data(self, **kwargs):
        context = super(VistaComunidad, self).get_context_data(**kwargs)
        context["seccion_header"]="Comunidades";
        comuNombre=self.kwargs["comunidad"];
        comunidad = Comunidad.objects.all().get(slug=comuNombre);
        context["comunidad"]=comunidad;
        if comunidad:
            admins=comunidad.administradores.all();
            context["admins"]=admins;
            participantes=comunidad.participantes.all();
            context["participantes"]=participantes;
            talleres=comunidad.talleres.all();
            context["talleres"]=talleres;
            foro=Foro.objects.all().get(slug=comuNombre);
            context["foro"]=foro;
        return context

class Explora(TemplateView):
    template_name = 'ubicacion_comunidades.html'
    def get_context_data(self, **kwargs):
        context = super(Explora, self).get_context_data(**kwargs)
        context["seccion_header"]="Explora";
        return context

class Destacados(TemplateView):
    template_name = 'vista_destacados_comunidad.html'
    def get_context_data(self, **kwargs):
        context = super(Destacados, self).get_context_data(**kwargs)
        context["seccion_header"]="Destacados";
        return context

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

    def get_context_data(self, **kwargs):
        context = super(RegisterProfile, self).get_context_data(**kwargs)
        context["titulo1"]="Regístrate en Tulia";
        context["titulo2"]="¡Ya estás a un paso de pertenecer a nuestra comunidad!";
        context["titulo3"]="Paso 2: Acerca de tí ";
        return context;

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
