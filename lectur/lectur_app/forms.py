# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Field, HTML, Column, Div
from django.contrib.auth.models import User
from lectur_app.models import Lector, Taller, Trabajo_Escrito, Espacio, Evento, Comunidad, Tema
from django.contrib.auth.forms import AuthenticationForm
from datetimewidget.widgets import DateTimeWidget


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_tag = False
    username = forms.CharField(
        label = "Nombre de Usuario | minúsculas",
        required = True,
         widget=forms.TextInput(attrs={'placeholder': 'pepitoperez','onchange':'nombreUsuario()'}),
    )
    first_name = forms.CharField(
        label = "Nombre",
        required = True,

         widget=forms.TextInput(attrs={'placeholder': 'Pepito'}),
    )
    last_name = forms.CharField(
        label = "Apellido",
        required = True,
         widget=forms.TextInput(attrs={'placeholder': 'Peréz'}),
    )
    email = forms.EmailField(
        label = "Correo electrónico",
        required = True,
         widget=forms.TextInput(attrs={'placeholder': 'pepitoperez@tulia.com','onchange':'correoUsuario()'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label = "Contraseña",
        required = True,
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
              HTML("<div></div>"),
              HTML("<h3 class='header-formulario'>Regístrate en Tulia</h3>"),
              HTML("<h4 class='header-formulario'>Para formar parte de nuestra comunidad debes estar registrado. Sólo debes completar los 2 formularios que se mostrarán a continuación. </h4>"),
              HTML("<h3 class='header-formulario'>Paso 1: Información de contacto </h3>"),
              HTML("<div class='elemento_formulario'>"),
                'username',
              HTML("</div><div class='elemento_formulario'>"),
                'first_name',
              HTML("</div><div class='elemento_formulario'>"),
                'last_name',
              HTML("</div><div class='elemento_formulario'>"),
                'email',
              HTML("</div><div class='elemento_formulario'>"),
                'password',
                HTML("</div><div class='elemento_formulario'>"),
                  HTML(' <label for="id_password" class="control-label requiredField"> Confirma tu contraseña<span class="asteriskField">*</span> </label>  <input type="password" name="confirmacion">'),
              HTML("</div><div class='elemento_formulario'>"),
                ButtonHolder(Submit('submit', 'Continuar', css_class='boton-formulario'),  css_class=' text-center'),
              HTML("</div><div class='elemento_formulario'>"),
                Div(
                    HTML('<div class="elemento_formulario"> <label>¿Ya eres miembro? <br> <a class="enlace_rojo" href="/inicia_sesion/">Inicia sesión</a></label>  </div>'),
                    css_class='field-bottom topborder padt15 text-center'
                ),
              HTML("</div>"),
                css_class='large-6 medium-8 medium-centered columns',
            ),
        )

class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_tag = False

    username = forms.CharField(
        label = "Usuario",
        required = True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label = "Contraseña",
        required = True,
    )


    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
              HTML("<div></div>"),
               HTML("<h3 class='header-formulario'>Iniciar sesión</h3> <h4>¡En Tulia hay tertulias!</h4>"),
              HTML("<div class='elemento_formulario'>"),
                'username',
              HTML("</div><div class='elemento_formulario'>"),
                'password',
              HTML("</div><div class='elemento_formulario'>"),

                ButtonHolder(Submit('submit', 'Iniciar sesión', css_class='boton-formulario'), css_class=' text-center'),
                Div(
                    HTML('<p>Eres nuevo en Tulia? <a href="/registrate/">Regístrate</a> </p>'),
                    css_class='field-bottom topborder padt15 text-center'
                ),
                css_class='large-4 medium-4 large-centered medium-centered columns',
            ),
        )


class LectorForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    descripcion = forms.CharField(
        label = "Sobre tí",
        required = True,
        max_length = 140,
        widget = forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre las actividades que realizas en tu tiempo libre.','onchange':'descripcionUsuario()','rows':'4'}),
    )

    imagen = forms.ImageField(
        label = "Cambiar Imagen",
        required = False,
        widget=forms.FileInput,
    )

    facebook = forms.CharField(
        label = "Facebook (Opcional)",
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://www.facebook.com/pepito.perez' }),
    )

    twitter = forms.CharField(
        label = "Twitter (Opcional)",
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://twitter.com/pepitoperez' }),
    )

    class Meta:
        model = Lector
        fields = ('descripcion', 'imagen', 'facebook', 'twitter')


    def __init__(self, *args, **kwargs):
        super(LectorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
              HTML("<div></div>"),
              HTML("<h3 class='header-formulario'>{{titulo1}}</h3>"),
              HTML("<h4 class='header-formulario'>{{titulo2}} </h4>"),
              HTML("<h3 class='header-formulario'>{{titulo3}}</h3>"),
              HTML("<div class='elemento_formulario'>"),

              HTML("<img class='' src= {% if user.lector %}'{{ user.lector.imagen.url }}' {% else %} {% load staticfiles %} '{% static 'imagenes/imagen_defecto.png' %}'{% endif %} > <div class='img_oculto'>"),
              'imagen',
              HTML("</div></div>"),
              Fieldset(
                "",
              HTML("<div class='elemento_formulario'>"),
              HTML("<h3 class='custom-header'>{{user.first_name}} {{user.last_name}}</h3>"),

              HTML("</div><div class='elemento_formulario'>"),
              'descripcion',
              HTML("</div><div class='elemento_formulario red_social'>"),
              'facebook',
              HTML("</div><div class='elemento_formulario red_social'>"),
              'twitter',
              HTML("</div>"),
              ButtonHolder(Submit('submit', 'Guardar cambios', css_class='boton-formulario')),
              css_class='large-5 medium-5 columns',
                ),

            )
        )

class ComunidadForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    nombre = forms.CharField(
        label = "Nombre",
        required = True,
        max_length = 20,
        )

    descripcion = forms.CharField(
        label = "Sobre tu comunidad",
        required = True,
        max_length = 200,
        widget = forms.Textarea(attrs={'placeholder': 'Cuéntanos que quieres realizar en tu comunidad.','rows':'4'}),
        )

    imagen = forms.ImageField(
        label = "Cambiar Imagen",
        required = False,
        widget=forms.FileInput,
    )

    class Meta:
        model = Comunidad
        fields = ('nombre', 'descripcion', 'imagen')

    def __init__(self, *args, **kwargs):
        super(ComunidadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
                HTML("<div></div>"),
                HTML("<h3 class='header-formulario'>{{titulo1}}</h3>"),
                HTML("<h4 class='header-formulario'>{{titulo2}} </h4>"),
                HTML("<div class='elemento_formulario'>"),

                HTML("<img class='' src= {% if comunidad and comunidad.imagen  %}'{{ comunidad.imagen.url }}' {% else %} {% load staticfiles %} '{% static 'imagenes/imagen_defecto.png' %}'{% endif %} > <div class='img_oculto'>"),
                'imagen',
                HTML("</div></div>"),
                Fieldset(
                "",
                HTML("<div class='elemento_formulario'>"),

                'nombre',
                HTML("</div><div class='elemento_formulario'>"),
                'descripcion',
                HTML("</div>"),
                ButtonHolder(Submit('submit', 'Guardar cambios', css_class='boton-formulario')),
                css_class='large-5 medium-5 columns',
        ),

    )
)

class TallerComunidadForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    fecha = forms.DateField(
        label = "Fecha",
        initial = "Selecciona la fecha en que se realizará la actividad",
        required = True,
        widget= forms.SelectDateWidget( ),
        )

    nombre = forms.CharField(
        label = "Nombre",
        required = True,
        max_length = 100,
        )

    descripcion = forms.CharField(
        label = "Sobre el taller",
        required = True,
        max_length = 400,
        widget = forms.Textarea(attrs={'placeholder': 'Cuéntanos acerca de la actividad.','rows':'4'}),
        )

    imagen = forms.ImageField(
        label = "Cambiar Imagen",
        required = False,
        widget=forms.FileInput,
        )

    cupos = forms.IntegerField(
        label = "Cupos del taller",
        required = True,
        )

    class Meta:
        model = Taller
        fields = ('fecha', 'nombre', 'descripcion', 'imagen', 'cupos')

    def __init__(self, *args, **kwargs):
        super(TallerComunidadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
                HTML("<div></div>"),
                HTML("<h3 class='header-formulario'>{{titulo1}}</h3>"),

                HTML("<div class='elemento_formulario'>"),

                HTML("<img class='' src= {% if taller and taller.imagen  %}'{{ taller.imagen.url }}' {% else %} {% load staticfiles %} '{% static 'imagenes/imagen_defecto.png' %}'{% endif %} > <div class='img_oculto'>"),
                'imagen',
                HTML("</div></div>"),
                Fieldset(
                "",
                HTML("<div class='elemento_formulario'>"),

                'nombre',
                HTML("</div><div class='elemento_formulario'>"),
                'descripcion',
                HTML("</div><div class='elemento_formulario'>"),
                'fecha',
                HTML("</div><div class='elemento_formulario'>"),
                'cupos',
                HTML("</div>"),
                ButtonHolder(Submit('submit', 'Guardar cambios', css_class='boton-formulario')),
                css_class='large-5 medium-5 columns',
        ),

    )
)

class EspacioForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    tipo = forms.IntegerField(
        label = "Tipo",
        required = True,
        )

    nombre = forms.CharField(
        label = "Nombre",
        required = True,
        max_length = 20,
        )

    descripcion = forms.CharField(
        label = "Sobre tu comunidad",
        required = True,
        max_length = 300,
        widget = forms.Textarea(attrs={'placeholder': 'Cuéntanos acerca de este lugar.','rows':'4'}),
        )
    direccion = forms.CharField(
        label = "Lugar",
        required = True,
        max_length = 40,
        widget = forms.Textarea(attrs={'placeholder': 'Dirección del lugar.','rows':'4'}),
        )

    latitud = forms.DecimalField(
        label = "Latitud",
        required = True,
        )

    longitud = forms.DecimalField(
        label = "Longitud",
        required = True,
        )

    class Meta:
        model = Espacio
        fields = ('tipo', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud')

    def __init__(self, *args, **kwargs):
        super(EspacioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
                HTML("<div></div>"),
                HTML("<h3 class='header-formulario'>{{titulo1}}</h3>"),
                Fieldset(
                "",
                HTML("<div class='elemento_formulario'>"),
                'nombre',
                HTML("<div class='elemento_formulario hiddenx'>"),
                'tipo',
                HTML("</div><div class='elemento_formulario'>"),
                HTML("<label class='control-label requiredField'> Tipo de lugar <span class='asteriskField'>*</span> </label> <div id='seleccionar_tipo'></div>"),
                HTML("</div><div class='elemento_formulario'>"),
                'descripcion',
                HTML("</div><div class='elemento_formulario'>"),
                'direccion',
                HTML("</div><div class='elemento_formulario'>"),
                HTML("<label class='control-label requiredField'> Ubícanos en el mapa  <span class='asteriskField'>*</span> </label> <div id='seleccionar_mapa'> Mapa </div>"),
                HTML("</div><div class='elemento_formulario hiddenx'>"),
                'latitud',
                'longitud',
                HTML("</div>"),
                ButtonHolder(Submit('submit', 'Guardar cambios', css_class='boton-formulario')),
                css_class='large-5 medium-5 columns',
        ),

    )
)

class TemaForoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    titulo = forms.CharField(
        label = "Título",
        required = True,
        max_length = 50,
        )

    mensaje = forms.CharField(
        label = "Agrega el contenido de tu entrada",
        required = True,
        max_length = 400,
        widget = forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre qué se va a discutir.','rows':'4'}),
        )

    class Meta:
        model = Tema
        fields = ('titulo', 'mensaje')

    def __init__(self, *args, **kwargs):
        super(TemaForoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
                HTML("<div></div>"),
                HTML("<h3 class='header-formulario'>{{titulo1}}</h3>"),
                HTML("<div class='elemento_formulario'> sasdadasdasdasd"),
                'titulo',
                HTML("</div><div class='elemento_formulario'>"),
                'mensaje',
                HTML("</div> "),
                ButtonHolder(Submit('submit', 'Guardar cambios', css_class='boton-formulario') ),
                css_class='large-5 medium-5 columns',
    ),

)
