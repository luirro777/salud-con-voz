# signals.py (versión corregida)
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


def _normalize_val(value):
    """
    Normaliza el valor recibido para comparar con las keys del mapper:
    - intenta convertir strings numéricas a int
    - si es Decimal o numpy int-like, convertir a int cuando sea seguro
    - si no se puede normalizar, devuelve None
    """
    if value is None:
        return None

    # Ya es entero
    if isinstance(value, int):
        return value

    # Decimal
    try:
        from decimal import Decimal
        if isinstance(value, Decimal):
            # solo convertir si es entero (ej 1.0 -> 1), sino devolver None
            try:
                ival = int(value)
                if ival == value:
                    return ival
                return None
            except Exception:
                return None
    except Exception:
        pass

    # numpy ints (si hay)
    try:
        import numbers
        if isinstance(value, numbers.Integral):
            return int(value)
    except Exception:
        pass

    # strings que contienen un entero
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            return int(s)
        # también admitir '-1' etc.
        try:
            ival = int(s)
            return ival
        except Exception:
            return None

    # fallback: no normalizable
    return None


def calcular_promedio(instance, mapper):
    """
    Calcula el promedio de los campos IntegerField del modelo
    usando el mapper proporcionado.
    - itera solo sobre instance._meta.fields (campos concretos)
    - normaliza cada valor antes de mapear
    - retorna float redondeado a 2 decimales
    """
    suma = 0.0
    count = 0

    # usar fields concretos del modelo (evita relaciones reversas, etc.)
    for field in instance._meta.fields:
        # filtrar IntegerField y sus subclases
        if not isinstance(field, models.IntegerField):
            continue
        # evitar pk/autofields
        if getattr(field, "primary_key", False) or getattr(field, "auto_created", False):
            continue

        # obtener valor y normalizar
        try:
            raw = getattr(instance, field.name)
        except Exception:
            continue

        v = _normalize_val(raw)
        if v is None:
            # valor no normalizable o None -> no contamos
            continue

        mapped = mapper.get(v)
        if mapped is None:
            # Valor fuera de mapeo: no contamos. Si querés debuggear,
            # aquí podés loguear raw/field.name para investigar.
            # e.g. logger.debug("No mapeado", field.name, raw)
            continue

        suma += mapped
        count += 1

    promedio = round(suma / count, 2) if count > 0 else 0.0
    return promedio


# Señales para cada modelo (normales)
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
    Se normaliza cada valor y se cuenta solo si el mapeo existe.
    """
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

    suma = 0.0
    count = 0
    for campo, mapper in mapeo_por_campo.items():
        try:
            raw = getattr(instance, campo)
        except AttributeError:
            # campo no existe en el modelo (posible inconsistencia en versiones)
            continue

        v = _normalize_val(raw)
        if v is None:
            continue

        mapped = mapper.get(v)
        if mapped is None:
            continue

        suma += mapped
        count += 1

    instance.promedio = round(suma / count, 2) if count > 0 else 0.0



