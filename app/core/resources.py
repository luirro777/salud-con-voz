from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Cpqol

class CpqolResource(resources.ModelResource):


    class Meta:
        model = Cpqol
        fields = (
            'creacion',
            'codigo',
            'sentimientos',
            'relaciones',
            'familia',
            'participacion',
            'escuela',
            'salud',
            'dolor',
            'servicios',
            )

    def dehydrate_sentimientos(self, obj): return obj.sentimientos.promedio()
    def dehydrate_relaciones(self, obj): return obj.relaciones.promedio()
    def dehydrate_familia(self, obj): return obj.familia.promedio()
    def dehydrate_participacion(self, obj): return obj.participacion.promedio()
    def dehydrate_escuela(self, obj): return obj.escuela.promedio()
    def dehydrate_salud(self, obj): return obj.salud.promedio()
    def dehydrate_dolor(self, obj): return obj.dolor.promedio()
    def dehydrate_servicios(self, obj): return obj.servicios.promedio()
