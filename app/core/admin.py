from django.contrib import admin
from .models import Cpqol, CpqolProfesional
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class CpqolResource(resources.ModelResource):

    class Meta:
        model = Cpqol  # or 'core.Cpqol'
        fields = (
			'creacion',
			'user__username',
			'codigo',
			'tutor__edad',
			'tutor__relacion',
			'tutor__quien_cuida',
			'tutor__estudios_alcanzados',
            'tutor__estado_salud',
			'paciente__edad',
			'paciente__genero',
			'paciente__provincia',
			'paciente__ciudad',
			'paciente__cobertura',
			'movimiento__movimiento',
			'sentimientos__hacer_cosas',
			'sentimientos__uno_mismo',
			'sentimientos__motivacion',
			'sentimientos__oportunidades',
			'sentimientos__aspecto_fisico',
			'relaciones__con_gente',
			'relaciones__otros_chichos',
			'relaciones__con_adultos',
			'relaciones__con_amigos',
			'relaciones__aceptacion_otros_chicos',
			'relaciones__aceptacion_adultos',
			'relaciones__aceptacion_gente',
			'relaciones__cosas_nuevas',
			'relaciones__comunicacion_conocidos',
			'relaciones__comunicacion_extranios',
			'relaciones__comunicacion_otros_con_el',
			'relaciones__comunicacion_tecnologia',
			'familia__apoyo_flia',
			'familia__viaje_flia',
			'familia__aceptacion_flia',
			'participacion__recreativas',
			'participacion__deportivas',
			'participacion__eventos_sociales',
			'participacion__en_su_comunidad',
			'escuela__otros_chicos_escuela',
			'escuela__como_lo_integran',
			'escuela__profesores',
			'escuela__otros_alumnos',
			'escuela__otros_docentes',
			'escuela__mismo_trato',
			'escuela__participacion_colegio',
			'salud__hacer_cosas_solo',
			'salud__movilidad',
			'salud__independencia',
			'salud__moverse_dentro_barrio',
			'salud__transporte',
			'salud__brazos_y_manos',
			'salud__piernas',
			'salud__vestirse',
			'salud__beber',
			'salud__ir_al_banio',
			'dolor__salud_gral',
			'dolor__suenio',
			'dolor__cuanto_dolor',
			'dolor__nivel_dolor',
			'dolor__nivel_incomodidad',
			'dolor__como_afecta',
			'dolor__impedimentos',
			'dolor__no_disfrutar_dia',
			'servicios',
			'servicios__acceso_tratamiento',
			'servicios__acceso_terapia',
			'servicios__acceso_atencion_medica',
			'servicios__acceso_pediatria',
			'servicios__acceso_ayuda_aprendizaje',     
		)
        

        export_order = '-creacion'

class CpqolProfesionalResource(resources.ModelResource):
    class Meta:
        model = CpqolProfesional  # o 'core.Cpqol'
        # Campos a importar/exportar, siguiendo la convención de doble guión bajo para relaciones
        fields = (
            'creacion',
            'user__username',
            'codigo',

            # Sección Profesional
            'profesional__profesion',
            'profesional__provincia_atencion',
            'profesional__ciudad_atencion',
            'profesional__tipo_centro',
            'profesional__centro_salud',

            # Sección Contexto
            'contexto__persona_ocupa',
            'contexto__max_estudios',
            'contexto__edad',
            'contexto__genero',

            # Sección Datos Clínicos
            'datos_clinicos__macs',
            'datos_clinicos__cfcs',
            'datos_clinicos__edacs',
        )
        # Controla el orden de las columnas al exportar
        export_order = fields

class CpqolAdmin(ImportExportModelAdmin):
	list_display = ['codigo', 'user', ]
	list_filter = ['user']
	resource_classes = [CpqolResource]
     
class CpqolProfesionalAdmin(ImportExportModelAdmin):
	list_display = ['codigo', 'user', ]
	list_filter = ['user']
	resource_classes = [CpqolProfesionalResource]

admin.site.register(Cpqol, CpqolAdmin)
admin.site.register(CpqolProfesional, CpqolProfesionalAdmin)