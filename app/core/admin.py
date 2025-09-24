from django.contrib import admin
from django.utils.html import format_html
from .models import Cpqol, CpqolProfesional

@admin.register(Cpqol)
class CpqolAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'user', 'creacion', 'completado', 'current_seccion']
    list_filter = ['completado', 'creacion', 'user']
    search_fields = ['codigo', 'user__username']
    readonly_fields = ['informacion_completa', 'creacion', 'current_seccion', 'estado_secciones_display']
    
    fieldsets = (
        ('Información General', {
            'fields': ('user', 'codigo', 'creacion', 'completado', 'current_seccion')
        }),
        ('Estado de Secciones', {
            'fields': ('estado_secciones_display',)
        }),
        ('Información Completa', {
            'fields': ('informacion_completa',)
        }),
    )
    
    def estado_secciones_display(self, obj):
        """Muestra el estado de cada sección de forma legible"""
        estado = obj.estado_secciones()
        secciones = []
        for seccion, completada in estado.items():
            icon = "✅" if completada else "❌"
            secciones.append(f"{icon} {seccion}: {'Completada' if completada else 'Pendiente'}")
        return format_html("<br>".join(secciones))
    
    estado_secciones_display.short_description = "Estado de Secciones"
    
    def has_add_permission(self, request):
        """Evita que se puedan agregar CPQOL manualmente desde el admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Evita que se modifiquen los CPQOL existentes desde el admin"""
        return False

@admin.register(CpqolProfesional)
class CpqolProfesionalAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'user', 'creacion', 'completado']
    list_filter = ['completado', 'creacion', 'user']
    search_fields = ['codigo', 'user__username']
    readonly_fields = ['creacion']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False