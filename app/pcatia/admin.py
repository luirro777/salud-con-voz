
from django.contrib import admin
from .models import Solicitud

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('fecha_solicitud', 'apellidos_principal', 'nombres_principal', 'titulo_estudio')
    search_fields = ('apellidos_principal', 'nombres_principal', 'titulo_estudio')
    list_filter = ('fecha_solicitud', 'institucion_principal')
    ordering = ('-fecha_solicitud',)