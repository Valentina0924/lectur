# -*- encoding: utf-8 -*-
from django.shortcuts import render
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
from datetime import datetime, timedelta, time
from django.db.models import Count

from django.views.generic import View, FormView, UpdateView, CreateView, DetailView, ListView, TemplateView
from lectur_app.forms import UserForm, LectorForm, UserLoginForm, ComunidadForm, TallerComunidadForm, EspacioForm, TemaForoForm;
from lectur_app.models import Lector, Comunidad, Foro, Taller, Categoria, Espacio, Respuesta, Tema, Premio, Reto, Notificacion, Genero_literario, Felicitacion

from django.conf import settings

from django.template import defaultfilters;
from django.template.defaultfilters import slugify;


def cantComunidadesMiembro(lector):
    comunidades= set([]);
    for com in Comunidad.objects.all():
        if lector in com.administradores.all():
            comunidades.add(com);
        if lector in com.participantes.all():
            comunidades.add(com);
    return len(comunidades);

def ingresarComunidadPremio (lector):
    retos=Reto.objects.filter(slug="miembro");
    for re in retos:
        premios =Premio.objects.filter(reto=re).order_by('cantidad_minima');
        for pre in premios:
            if not lector in pre.lista_ganadores.all():
                if pre.cantidad_minima <= cantComunidadesMiembro(lector)  :
                    pre.lista_ganadores.add(lector);
                    pre.save();

                    noti=Notificacion(imagen=pre.imagen , contenido="Logro completado: "+pre.titulo, usuario=lector.user)
                    noti.save();
                    feli=Felicitacion(imagen=pre.imagen , contenido="Felicidades has completado el logro "+pre.titulo, usuario=lector.user)
                    feli.save();
                    print ("unido");
                    return True;
    return False;


def cantTemasMiembro(lector):
    temas= set(Tema.objects.filter(autor = lector));
    return len(temas);

def crearTemaPremio (lector):
    retos = Reto.objects.filter(slug="anfitrion");
    for re in retos:
        premios = Premio.objects.filter(reto=re).order_by('cantidad_minima');
        for pre in premios:
            if not lector in pre.lista_ganadores.all():
                if pre.cantidad_minima <= cantTemasMiembro(lector):
                    pre.lista_ganadores.add(lector);
                    pre.save();
                    noti=Notificacion(imagen=pre.imagen , contenido="Logro completado: "+pre.titulo, usuario=lector.user)
                    noti.save();
                    feli=Felicitacion(imagen=pre.imagen , contenido="Felicidades has completado el logro "+pre.titulo, usuario=lector.user)
                    feli.save();
                    print ("creado");
                    return True;
    return False;

def cantComentariosMiembro(lector):
    comentarios = set(Respuesta.objects.filter(perfil = lector));
    return len(comentarios);

def comentaPorPremio (lector):
        retos = Reto.objects.filter(slug="participante");
        for re in retos:
            premios = Premio.objects.filter(reto=re).order_by('cantidad_minima');
            for pre in premios:
                if not lector in pre.lista_ganadores.all():
                    if pre.cantidad_minima <= cantComentariosMiembro(lector):
                        pre.lista_ganadores.add(lector);
                        pre.save();
                        noti=Notificacion(imagen=pre.imagen , contenido="Logro completado: "+pre.titulo, usuario=lector.user)
                        noti.save();
                        feli=Felicitacion(imagen=pre.imagen , contenido="Felicidades has completado el logro "+pre.titulo, usuario=lector.user)
                        feli.save();
                        print ("creado");
                        return True;
        return False;

@login_required
def ver_notificaciones(request,username):
    s="/respuestajax/Notificaciones eliminadas";
    usu = User.objects.get(username=username);
    notificaciones = Notificacion.objects.filter(usuario=usu);
    for notificacion in notificaciones:
        notificacion.estado = 0;
        notificacion.save();

    return  HttpResponseRedirect(s);

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
        return "/comunidades/"

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
        context["premios"]=getPremiosUsuario(lec);
        return context;

@login_required
def unirActividad(request, username, taller):
    usu = User.objects.get(username=username);
    perfil = Lector.objects.get(user=usu);
    taller = Taller.objects.get(slug=taller);
    s="/respuestajax/";
    tipo=request.GET["tipo"];
    mensaje="";
    if tipo=="unir":
        taller.participantes.add(perfil);
        mensaje="Te has registrado al taller: "+taller.nombre;
    elif tipo=="salir":
        taller.participantes.remove(perfil);
        mensaje="Has salido del taller "+taller.nombre;

    s+=mensaje;
    noti=Notificacion(imagen=taller.imagen , contenido=mensaje, usuario=perfil.user)
    noti.save();
    taller.save();
    return  HttpResponseRedirect(s);


class Comunidades(TemplateView):
    template_name = 'explora_comunidades.html'
    def get_context_data(self, **kwargs):
        context = super(Comunidades, self).get_context_data(**kwargs)
        context["seccion_header"]="Comunidades";

        lec = Lector.objects.all().get(user=self.request.user);
        comunidades= set([]);
        for com in Comunidad.objects.all():
            for adm in com.administradores.all():
                if adm==lec:
                    comunidades.add(com);
            for par in com.participantes.all():
                if par==lec:
                    comunidades.add(com);

        context["comunidades"] =comunidades;


        # user = self.request.user;
        # lector = Lector.objects.get(user=user);
        context["premios"]=getPremiosUsuario(lec);


        talleres=set([]);
        for act in Taller.objects.all().filter(fecha__gte = datetime.now()).order_by('fecha'):
            for par in act.participantes.all():
                if par ==lec:
                    talleres.add(act);
        context["talleres"] =talleres;
        return context;

def getPremiosUsuario(lector):
    premios={};
    pre=Premio.objects.all();
    for p in pre:
        if lector in p.lista_ganadores.all():
            if premios.get(p.reto):
                premios[p.reto].append(p);
            else:
                premios[p.reto]=[p];

    return premios;

class VistaComunidad(TemplateView):
    template_name = 'vista_comunidad.html'
    def get_context_data(self, **kwargs):
        context = super(VistaComunidad, self).get_context_data(**kwargs)
        context["seccion_header"]="Comunidades";
        comuNombre=self.kwargs["comunidad"];

        if "tipo" in self.kwargs and kwargs["tipo"]:
            tipo=self.kwargs["tipo"];
            context["tipo"]=tipo;
        else:
            tipo="actividades";
        comunidad = Comunidad.objects.all().get(slug=comuNombre);
        context["comunidad"]=comunidad;
        if comunidad:
            admins=comunidad.administradores.all().order_by('user__first_name');
            context["admins"]=admins;
            participantes=comunidad.participantes.all().order_by('user__first_name');
            context["participantes"]=participantes;
            talleres=comunidad.talleres.all();
            context["talleres"]=talleres;
            foro=Foro.objects.all().get(slug=comuNombre);
            context["foro"]=foro;

            pertenece=0;
            if self.request.user and self.request.user.is_authenticated:
                    lect=Lector.objects.get(user=self.request.user)
                    if lect in admins:
                        pertenece=2;
                    if pertenece ==0:
                        if lect in participantes:
                            pertenece=1;
            else:
                pertenece=-1;
            context["pertenece"]=pertenece;

        return context

class Explora(TemplateView):
    template_name = 'ubicacion_comunidades.html'
    def get_context_data(self, **kwargs):
        context = super(Explora, self).get_context_data(**kwargs)
        context["seccion_header"]="Explora";
        comunidades=Comunidad.objects.all();
        context["comunidades"]=comunidades;
        context["categorias"]=Genero_literario.objects.all();


        return context

class VistaForo(TemplateView):
    template_name = 'vista_foro.html'

    def get_context_data(self, **kwargs):
        context = super(VistaForo, self).get_context_data(**kwargs)
        foroNombre=self.kwargs["foro"];
        context["seccion_header"]="Foro";
        foro=Foro.objects.all().get(slug=foroNombre);
        context["foro"]=foro;

        comunidad=Comunidad.objects.all().get(slug=foroNombre);
        context["comunidad"]=comunidad;
        return context

class VistaCategoriaForo(TemplateView):
    template_name = 'vista_categoria_foro.html'

    def get_context_data(self, **kwargs):
        context = super(VistaCategoriaForo, self).get_context_data(**kwargs)
        foroNombre=self.kwargs["foro"];
        foroCategoria=self.kwargs["categoria"];
        context["seccion_header"]="Foro";
        foro=Foro.objects.all().get(slug=foroNombre);
        context["foro"]=foro;
        categoria= foro.categoria.all().get(slug=foroCategoria);
        context["categoria"]= categoria;
        comunidad=Comunidad.objects.all().get(slug=foroNombre);
        context["comunidad"]=comunidad;
        return context

class VistaTemaForo(TemplateView):
    template_name = 'vista_tema_foro.html'

    def get_context_data(self, **kwargs):
        context = super(VistaTemaForo, self).get_context_data(**kwargs)
        foroNombre=self.kwargs["foro"];
        foroCategoria=self.kwargs["categoria"];
        categoriaTema=self.kwargs["tema"];
        context["seccion_header"]="Foro";
        foro=Foro.objects.all().get(slug=foroNombre);
        context["foro"]=foro;
        categoria= foro.categoria.all().get(slug=foroCategoria);
        context["categoria"]= categoria;
        tema= categoria.tema.all().get(slug=categoriaTema);
        context["tema"]=tema;
        comunidad=Comunidad.objects.all().get(slug=foroNombre);
        context["comunidad"]=comunidad;

        respuestas= tema.respuesta.all().filter(tipo_respuesta=-1);
        context["respuestas"]=respuestas;

        return context

@login_required
def register_comment(request, username, pk):

    usu = User.objects.get(username=username);
    perfil = Lector.objects.get(user=usu);
    mensaje=request.GET["mensaje"];
    tipo=request.GET["tipo"];
    s='/vista-comentario/';

    comentaPorPremio(perfil);

    if tipo=="respuesta":
        tema=Tema.objects.get(pk=pk);
        nueva_respuesta=Respuesta(perfil=perfil, mensaje=mensaje, tipo_respuesta=-1);
        nueva_respuesta.save();
        tema.respuesta.add(nueva_respuesta);
        tema.save();
        s+=str(nueva_respuesta.pk);
    elif tipo=="comentario":
        nueva_respuesta=Respuesta(perfil=perfil, mensaje=mensaje, tipo_respuesta=int(pk));
        nueva_respuesta.save();
        s+=str(nueva_respuesta.pk);
    return  HttpResponseRedirect(s);

@login_required
def registrarUsuarioComunidad(request, username, comunidad):
    usu = User.objects.get(username=username);
    perfil = Lector.objects.get(user=usu);
    comunidad = Comunidad.objects.get(slug=comunidad);
    s="/respuestajax/";
    tipo=request.GET["tipo"];
    if tipo=="unir":
        comunidad.participantes.add(perfil);
        ingresarComunidadPremio(perfil);
        s+="Te has unido a "+comunidad.nombre;
    elif tipo=="salir":
        comunidad.participantes.remove(perfil);
        s+="Has salido de "+comunidad.nombre;
    elif tipo=="u_admin":
        comunidad.participantes.remove(perfil);
        comunidad.administradores.add(perfil);
        s+=usu.first_name+" "+usu.last_name+" ha sido promovido a Administrador"
    elif ripo=="s_admin":
        comunidad.administradores.remove(perfil);
        s+="Has salido de "+comunidad.nombre;
    comunidad.save();
    return  HttpResponseRedirect(s);

class Vistajax(TemplateView):
    template_name = 'vista_respuestaajax.html'
    def get_context_data(self, **kwargs):
        context = super(Vistajax, self).get_context_data(**kwargs)
        context["respuesta"]=self.kwargs["respuesta"];
        return context

class VistaComentario(TemplateView):
    template_name = 'respuesta_foro.html';
    def get_context_data(self, **kwargs):
        context = super(VistaComentario, self).get_context_data(**kwargs)
        respuesta=Respuesta.objects.get(pk=self.kwargs["pk"]);
        context["autor"]  =respuesta.perfil;
        context["mensaje"]  =respuesta.mensaje;
        context["fecha"]  =respuesta.fecha;
        context["pk"]  =respuesta.pk;
        context["isRespuesta"]  = respuesta.tipo_respuesta==-1;
        context["principal"]=true =respuesta.tipo_respuesta==-1;
        return context


class Destacados(TemplateView):
    template_name = 'vista_destacados_comunidad.html'
    def get_context_data(self, **kwargs):
        context = super(Destacados, self).get_context_data(**kwargs)
        context["seccion_header"]="Destacados";
        top_temas = Tema.objects.annotate(q_count=Count('respuesta')) \
                                 .order_by('-q_count');#[:10]


        context["temas"]=top_temas;

        return context

def get_codigo_nuevo_usuario():
    hoy = datetime.today();
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

        feli=Felicitacion(imagen=lector.imagen , contenido="Felicidades ya eres parte de Tulia ", usuario=lector.user)
        feli.save();
        return HttpResponseRedirect('/comunidades');

class UpdateProfile(UpdateView):
    """ Vista de la página de formulario donde se registra un nuevo usuario """
    template_name = 'register.html'
    form_class = LectorForm
    model = User
    state=False

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        context["titulo1"]="Actualiza tu perfil";
        #context["titulo2"]="";
        #context["titulo3"]="";
        return context;


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

class CrearComunidad(CreateView):
    """ Vista de la página de formulario donde se registra una nueva comunidad """
    template_name = 'register.html'
    form_class = ComunidadForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(CrearComunidad, self).get_context_data(**kwargs)
        context["titulo1"]="Registra tu comunidad";
        context["titulo2"]="¡Ya estás a un paso de crear tu comunidad!";

        return context;

    def form_valid(self, form):
        comunidad = form.save(commit=False);
        slugComu= defaultfilters.slugify(comunidad.nombre);
        comunidad.slug =slugComu;
        comunidad.save();


        usuario = self.request.user;
        administrador = Lector.objects.get(user=usuario);
        comunidad.administradores.add(administrador);
        comunidad.save();


        tituloForo="Foro de "+comunidad.nombre
        contenidoForo="Bienvenidos al foro de "+comunidad.nombre;
        comuForo=Foro( titulo =tituloForo , contenido = contenidoForo , slug=slugComu );
        comuForo.save();

        tituloDiscusion = "Discusión";
        descripcionDiscusion ="Discutimos temas de interés para la comunidad";
        slugDiscusion ="discusion-"+slugComu;
        cateDiscusion=Categoria(titulo=tituloDiscusion, descripcion=descripcionDiscusion, slug=slugDiscusion, tipo = 0);
        cateDiscusion.save();

        tituloCreacion = "Creación";
        descripcionCreacion = "Compartimos ideas para la creación de nuestros textos";
        slugCreacion = "creacion-"+slugComu;
        cateCreacion = Categoria(titulo=tituloCreacion, descripcion=descripcionCreacion, slug=slugCreacion, tipo = 1);
        cateCreacion.save();

        tituloRecomendacion = "Recomendación";
        descripcionRecomendacion = "Recomienda libros u autores que hayas leído";
        slugRecomendacion = "recomendacion-"+slugComu;
        cateRecomendacion = Categoria(titulo=tituloRecomendacion, descripcion=descripcionRecomendacion, slug=slugRecomendacion, tipo = 2);
        cateRecomendacion.save();

        comuForo.categoria.add(cateDiscusion);
        comuForo.categoria.add(cateCreacion);
        comuForo.categoria.add(cateRecomendacion);

        comuForo.save();
        form.save_m2m();
        return HttpResponseRedirect('/comunidades');

class CrearTaller(CreateView):
    """ Vista de la página de formulario donde se registra un nuevo taller """
    template_name = 'register.html'
    form_class = TallerComunidadForm
    model = Taller
    url_retorno="/comunidades/"

    def get_context_data(self, **kwargs):
        context = super(CrearTaller, self).get_context_data(**kwargs)
        context["titulo1"]="Crea una actividad para tu comunidad";
        nombrecomunidad=self.kwargs["comunidad"];
        url_retorno="/comunidades/"+nombrecomunidad;
        comunidad=Comunidad.objects.get(slug=nombrecomunidad);
        context["comunidad"]=comunidad;
        return context;

    def form_valid(self, form):
        nombrecomunidad=self.kwargs["comunidad"];
        url_retorno="/comunidades/"+nombrecomunidad;
        taller = form.save(commit=False);
        slugTaller= defaultfilters.slugify(taller.nombre);
        taller.slug =slugTaller;
        usuario = self.request.user;
        organizador = Lector.objects.get(user=usuario);
        taller.organizador = organizador;
        taller.save();


        comunidad=Comunidad.objects.get(slug=nombrecomunidad);
        comunidad.talleres.add(taller);
        comunidad.save();
        form.save_m2m();
        return HttpResponseRedirect(url_retorno);

class RegistrarEspacio(CreateView):
    """ Vista de la página de formulario donde se registra el espacio """
    template_name = 'registrar_ubicacion.html'
    form_class = EspacioForm
    model = Espacio
    url_retorno="/comunidades/"

    def get_context_data(self, **kwargs):
        context = super(RegistrarEspacio, self).get_context_data(**kwargs)
        context["titulo1"]="Agrega el espacio de encuentro de tu comunidad";
        nombrecomunidad=self.kwargs["comunidad"];
        url_retorno="/comunidades/"+nombrecomunidad;
        comunidad=Comunidad.objects.get(slug=nombrecomunidad);
        context["comunidad"]=comunidad;
        return context;

    def form_valid(self, form):
        nombrecomunidad=self.kwargs["comunidad"];
        url_retorno="/comunidades/"+nombrecomunidad;
        espacio = form.save(commit=True);
        comunidad=Comunidad.objects.get(slug=nombrecomunidad);
        comunidad.lugares_encuentro.add(espacio);
        comunidad.save();
        return HttpResponseRedirect(url_retorno);

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

class CrearTema(CreateView):
    """ Vista de la página de formulario donde se registra un nuevo tema """
    template_name = 'register.html'
    form_class = TemaForoForm
    model = Tema
    url_retorno="/comunidades/"

    def get_context_data(self, **kwargs):
        context = super(CrearTema, self).get_context_data(**kwargs)
        context["titulo1"]="Genera discusión creando un nuevo tema";
        nombrecomunidad=self.kwargs["comunidad"];
        url_retorno="/comunidades/"+nombrecomunidad;
        comunidad=Comunidad.objects.get(slug=nombrecomunidad);
        context["comunidad"]=comunidad;
        return context;

    def form_valid(self, form):
        tema = form.save(commit=False);
        slugTema= defaultfilters.slugify(tema.titulo);
        tema.slug =slugTema;
        usuario = self.request.user;
        autor = Lector.objects.get(user=usuario);
        tema.autor = autor;
        tema.save();

        nombrecomunidad=self.kwargs["comunidad"];
        nombrecategoria=self.kwargs["categoria"];
        categoria=Categoria.objects.get(slug=nombrecategoria);
        categoria.tema.add(tema);
        categoria.save();

        crearTemaPremio(autor);


        url_retorno="/foro/"+nombrecomunidad+"/"+nombrecategoria+"/"+slugTema;
        return HttpResponseRedirect(url_retorno);
