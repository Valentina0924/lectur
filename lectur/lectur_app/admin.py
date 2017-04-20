from django.contrib import admin
from lectur_app.models import Lector, Taller, Trabajo_Escrito, Espacio, Evento,  Comunidad, Valoracion, Respuesta, Tema, Categoria, Foro, Reto, Premio, Notificacion, Genero_literario

# Register your models here.
admin.site.register(Lector)
admin.site.register(Comunidad)
admin.site.register(Taller)
admin.site.register(Espacio)
admin.site.register(Evento)
admin.site.register(Trabajo_Escrito)

admin.site.register(Valoracion)
admin.site.register(Respuesta)
admin.site.register(Tema)
admin.site.register(Categoria)
admin.site.register(Foro)
admin.site.register(Reto)
admin.site.register(Premio)
admin.site.register(Notificacion)
admin.site.register(Genero_literario)
