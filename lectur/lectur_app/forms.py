# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Field, HTML, Column, Div
from django.contrib.auth.models import User
from lectur_app.models import Lector, Taller, Trabajo_Escrito, Espacio, Evento, Comunidad
from django.contrib.auth.forms import AuthenticationForm



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_tag = False
    username = forms.CharField(
        label = "Nombre de Usuario | minusculas",
        required = True,
    )
    first_name = forms.CharField(
        label = "Nombre",
        required = True,
    )
    last_name = forms.CharField(
        label = "Apellido",
        required = True,
    )
    email = forms.EmailField(
        label = "Correo electrónico",
        required = True,
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
               HTML("<h3 class='custom-header'>Regístrate en Tulia</h3>"),
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
                ButtonHolder(Submit('submit', 'Registrarse', css_class='btn_enviar'),  css_class=' text-center'),
              HTML("</div><div class='elemento_formulario'>"),
                Div(
                    HTML('<div class="elemento_formulario"> <label>¿Ya eres miembro? <br> <a class="enlace_rojo" href="/login/">Inicia sesion</a></label> <br>Conoce los <a href="#" class="enlace_negro">términos de servicio</a> </div>'),
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
               HTML("<h3 class='custom-header'>Iniciar sesión</h3> <h4>¡En Tulia hay tertulias!</h4>"),
              HTML("<div class='elemento_formulario'>"),
                'username',
              HTML("</div><div class='elemento_formulario'>"),
                'password',
              HTML("</div><div class='elemento_formulario'>"),

                ButtonHolder(Submit('submit', 'Iniciar sesión', css_class='btn_enviar'), css_class=' text-center'),
                Div(
                    HTML('<p>Eres nuevo en Tulia? <a href="/register/">Registrate</a> <br> Has olvidado tu contrasena? <a href="#" data-reveal-id="firstModal">Recuperar</a></p>'),
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
        widget = forms.Textarea
    )

    imagen = forms.ImageField(
        label = "Cambiar Imagen",
        required = False,
        widget=forms.FileInput,
    )

    facebook = forms.CharField(
        label = "Facebook (Opcional)",
        required=False,
        widget=forms.URLInput
    )

    twitter = forms.CharField(
        label = "Twitter (Opcional)",
        required=False,
        widget=forms.URLInput
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
              "",
              HTML("<div class='large-2 medium-2 columns elemento_formulario'> "),
              HTML("<img class='img-container-user-profile  circular' src= {% if user.userprofile.avatar_url %}'{{ user.userprofile.avatar_url.url_700x700 }}' {% else %} 'http://s22.postimg.org/sgwv8z7kx/url.jpg'{% endif %} style='width:100%;'> <div class='img_oculto'>"),
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
              ButtonHolder(Submit('submit', 'Guardar cambios', css_class='button radius btn_crearProyecto')),
              css_class='large-5 medium-5 columns',
                ),


            )
        )
