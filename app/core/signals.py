# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from .models import (
    Sentimientos, Relaciones, Familia, Participacion, 
    Escuela, Salud, Dolor, Servicios, Movimiento
)

# Mappers para los cálculos
MAPPER_NORMAL = {
    1: 0,
    2: 12.5,
    3: 25,
    4: 37.5,
    5: 50,
    6: 62.5,
    7: 75,
    8: 87.5,
    9: 100
}

MAPPER_INVERSO = {
    1: 100,
    2: 87.5,
    3: 75,
    4: 62.5,
    5: 50,
    6: 37.5,
    7: 25,
    8: 12.5,
    9: 0
}

MAPPER_MOVIMIENTO = {
    1: 0,
    2: 25,
    3: 50,
    4: 75,
    5: 100
}

def calcular_promedio(instance, mapper):
    """
    Calcula el promedio de los campos IntegerField del modelo
    usando el mapper proporcionado.
    """
    suma = 0
    count = 0
    fields = instance._meta.get_fields()
    
    for field in fields:
        if (isinstance(field, models.IntegerField) and 
            not field.primary_key and 
            not field.auto_created):
            value = getattr(instance, field.name)
            if value is not None and value in mapper:
                suma += mapper[value]
                count += 1
                
    return suma / count if count > 0 else 0

# Señales para cada modelo
@receiver(pre_save, sender=Sentimientos)
@receiver(pre_save, sender=Relaciones)
@receiver(pre_save, sender=Familia)
@receiver(pre_save, sender=Participacion)
@receiver(pre_save, sender=Escuela)
@receiver(pre_save, sender=Salud)
@receiver(pre_save, sender=Servicios)
def calcular_promedio_normal(sender, instance, **kwargs):
    instance.promedio = calcular_promedio(instance, MAPPER_NORMAL)

@receiver(pre_save, sender=Dolor)
def calcular_promedio_dolor(sender, instance, **kwargs):
    """
    Calcula el promedio para el modelo Dolor usando mapeo específico por campo.
    """
    # Definir qué campos usan qué mapeo
    mapeo_por_campo = {
        'salud_gral': MAPPER_NORMAL,
        'suenio': MAPPER_NORMAL,
        'cuanto_dolor': MAPPER_INVERSO,
        'nivel_dolor': MAPPER_INVERSO,
        'nivel_incomodidad': MAPPER_INVERSO,
        'como_afecta': MAPPER_INVERSO,
        'impedimentos': MAPPER_INVERSO,
        'no_disfrutar_dia': MAPPER_INVERSO
    }
    
    suma = 0
    count = 0
    
    for campo, mapper in mapeo_por_campo.items():
        try:
            value = getattr(instance, campo)
            if value is not None and value in mapper:
                suma += mapper[value]
                count += 1
        except AttributeError:
            # Si el campo no existe, continuar con el siguiente
            continue
    
    instance.promedio = round(suma / count, 2) if count > 0 else 0


@receiver(pre_save, sender=Movimiento)
def calcular_promedio_movimiento(sender, instance, **kwargs):
    if instance.movimiento in MAPPER_MOVIMIENTO:
        instance.promedio = MAPPER_MOVIMIENTO[instance.movimiento]
    else:
        instance.promedio = 0