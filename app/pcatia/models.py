from django.db import models
from django.utils import timezone

class Solicitud(models.Model):
    #Primero registro la fecha
    fecha_solicitud = models.DateTimeField(default=timezone.now)

    # Responsable principal
    nombres_principal = models.CharField(max_length=100)
    apellidos_principal = models.CharField(max_length=100)
    cargo_principal = models.CharField(max_length=100)
    institucion_principal = models.CharField(max_length=100)
    ciudad_principal = models.CharField(max_length=100)
    pais_principal = models.CharField(max_length=100)
    rol_estudio_principal = models.CharField(max_length=200)
    email_principal = models.EmailField()
    telefono_principal = models.CharField(max_length=20)    

    # Responsable alterno
    nombres_alterno = models.CharField(max_length=100)
    apellidos_alterno = models.CharField(max_length=100)
    cargo_alterno = models.CharField(max_length=100)
    institucion_alterno = models.CharField(max_length=100)
    ciudad_alterno = models.CharField(max_length=100)
    pais_alterno = models.CharField(max_length=100)
    rol_estudio_alterno = models.CharField(max_length=200)
    email_alterno = models.EmailField()
    telefono_alterno = models.CharField(max_length=20)

    # Información del estudio
    uso_curricular = models.CharField(max_length=3, choices=[('Sí', 'Sí'), ('No', 'No')], blank=False)
    carrera_posgrado = models.CharField(max_length=200, blank=True)
    estudiantes = models.CharField(max_length=200, blank=True)
    responsables_orientacion = models.CharField(max_length=200, blank=True)

    # Datos del proyecto
    titulo_estudio = models.CharField(max_length=200)
    objetivo = models.TextField(max_length=500)
    descripcion_metodologia = models.TextField(max_length=1500)
    caracteristicas_poblacion = models.TextField(max_length=500)
    utilidad_estudio = models.CharField(max_length=500)
    institucion_avala = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"{self.fecha_solicitud} - {self.apellidos_principal}, {self.nombres_principal}"