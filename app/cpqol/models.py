from django.db import models

# Create your models here.
class CPQOL(models.Model):
    
    nombre = models.CharField(max_length=300)
    apellido = models.CharField(max_length=300)
    is_activo = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField()