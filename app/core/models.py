from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Tutor(models.Model):
    
    edad = models.IntegerField()
    relacion = models.CharField(max_length=50)
    quien_cuida = models.CharField(max_length=100)
    estudios_alcanzados = models.CharField(max_length=100)
    CHOICES_SALUD = {
        'excelente': 'Excelente',
        'muy-buena': 'Muy buena',
        'buena': 'Buena',
        'regular': 'Regular',
        'mala': 'Mala',
    }
    estado_salud = models.CharField(max_length=20, choices=CHOICES_SALUD)

class Paciente(models.Model):
    edad = models.DateField()
    dni = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
    CHOICES_GENERO = {
        'mujer': 'Mujer',
        'varon': 'Varón',
        'otro': 'Otro',

    }
    genero = models.CharField(max_length=20, choices=CHOICES_GENERO)
    provincia = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    obra_social = models.CharField(max_length=30, blank=True, null=True)
    prepaga = models.CharField(max_length=30, blank=True, null=True)
    servicio_publico = models.CharField(max_length=30, blank=True, null=True)
    CHOICES_MOVIMIENTO = {
        1: 'Tiene dificultad para mantenerse sentado y para poder controlar la cabeza y el tronco en cualquier posición.',
        2: 'Puede mantenerse sentado con algún soporte en pelvis o en tronco, pero no estar de pie, ni caminar sin gran ayuda.',
        3: 'Es capaz de mantenerse de pie por sí mismo y de caminar, sólo si usa alguna ayuda para la marcha (como un andador, muletas, bastones, etc.)',
        4: 'Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamano para subir y bajar escaleras.',
        5: 'Puede caminar sin ayudas para la marcha y subir y bajar escaleras sin necesidad de apoyarse en el pasamano.',
    }
    movimiento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=CHOICES_MOVIMIENTO)



class CPQOL(models.Model):

    tutor = models.ForeignKey(Tutor, blank=True, null=True, on_delete=models.PROTECT)
    paciente = models.ForeignKey(Paciente, blank=True, null=True, on_delete=models.PROTECT)
