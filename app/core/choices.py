# choices.py
# Constantes para niveles educativos
CHOICES_NIVEL_EDUCATIVO = (
    ("1. No fue a la escuela", "1. No fue a la escuela"),
    ("2. Primaria incompleta (comenzó, pero no terminó la escuela primaria)", "2. Primaria incompleta (comenzó, pero no terminó la escuela primaria)"),
    ("3. Primaria completa", "3. Primaria completa"),
    ("4. Secundaria incompleta (comenzó, pero no terminó la secundaria)", "4. Secundaria incompleta (comenzó, pero no terminó la secundaria)"),
    ("5. Secundaria completa", "5. Secundaria completa"),
    ("6. Terciario o universitario incompleto (los comenzó, pero no los terminó)a", "6. Terciario o universitario incompleto (los comenzó, pero no los terminó)"),
    ("7. Terciario completo", "7. Terciario completo"),
    ("8. Universitario de grado completo o posgrado completo", "8. Universitario de grado completo o posgrado completo")
)

# Constantes para profesiones
CHOICES_PROFESION = [
    ("medico_familia", "Médico/a de familia/general"),
    ("medico_fisiatra", "Médico/a fisiatra"),
    ("medico_especialista", "Médico/a especialista"),
    ("fonoaudiologo", "Fonoaudiólogo/a"),
    ("kinesiologo", "Kinesiólogo/a"),
    ("terapista_ocupacional", "Terapista Ocupacional"),
    ("nutricionista", "Nutricionista"),
    ("psicologo", "Psicólogo/a"),
    ("trabajador_social", "Trabajador/a social"),
    ("docente_inclusion", "Docente de inclusión"),
    ("acompanante_terapeutico", "Acompañante terapéutica/o"),
    ("otra", "Otra"),
]

# Constantes para tipos de centros
CHOICES_TIPO_CENTRO = [
    ("centro_privado", "Centro o clínica privada"),
    ("centro_publico", "Hospital u otro tipo de centro público"),
    ("consultorio_particular", "Consultorio particular"),
    ("otro", "Otro ¿Cuál?"),
]

# Constantes para personas que ocupan
CHOICES_PERSONA_OCUPA = [
    ("madre", "Madre"),
    ("padre", "Padre"),
    ("tutor_legal", "Tutor/a legal"),
    ("pareja_madre_padre", "Pareja de la madre o el padre"),
    ("abuelo_abuela", "Abuela/o"),
    ("hermano_hermana", "Hermana/o"),
    ("otro_familiar", "Otro familiar ¿Cuál?"),
    ("otra_persona_no_familiar", "Otra persona, no familiar ¿Cuál?"),
]

# Constantes para género
CHOICES_GENERO = [
    ("femenino", "Femenino"),
    ("masculino", "Masculino"),
    ("no_binario", "No binario"),
    ("otro", "Otro ¿cuál?"),
]

# Constantes para niveles
CHOICES_NIVEL = [
    ("nivel_i", "Nivel I"),
    ("nivel_ii", "Nivel II"),
    ("nivel_iii", "Nivel III"),
    ("nivel_iv", "Nivel IV"),
    ("nivel_v", "Nivel V"),
]

# Constantes para sentimientos
CHOICES_SENTIMIENTOS = {
    1: '1 - Muy Desconforme',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9 - Muy Conforme',
}

# Constantes para dolor
CHOICES_DOLOR = {
    1: '1 - Nada de dolor',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9 - Mucho dolor',
}

# Constantes para molestia
CHOICES_MOLESTIA = {
    1: '1 - Nada molesto',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9 - Muy molesto',
}

# Constantes para opciones finales
CHOICES_FINALES = (
    ('Nunca', 'Nunca'),
    ('Casi Nunca', 'Casi Nunca'),
    ('Algunas Veces', 'Algunas Veces'),
    ('Casi Siempre', 'Casi Siempre'),
    ('Siempre', 'Siempre')
)

CHOICES_FINALES_2 = (
    ('No tiene problemas en ese aspecto', 'No tiene problemas en ese aspecto'),
    ('Nunca', 'Nunca'),
    ('Casi Nunca', 'Casi Nunca'),
    ('Algunas Veces', 'Algunas Veces'),
    ('Casi Siempre', 'Casi Siempre'),
    ('Siempre', 'Siempre')
)

# Constantes para sí/no
CHOICES_SI_NO = {
    "No": "No",
    "Si": "Si"
}

# Constantes para intensidad
CHOICES_INTENSIDAD = [
    ('Siempre', 'Siempre'),
    ('Casi siempre', 'Casi siempre'),
    ('Algunas veces', 'Algunas veces'),
    ('Casi nunca', 'Casi nunca'),
    ('Nunca', 'Nunca')
]

CHOICES_INTENSIDAD_2 = [
    ('Muchísimo', 'Muchísimo'),
    ('Mucho', 'Mucho'),
    ('Moderadamente', 'Moderadamente'),
    ('Un poco', 'Un poco'),
    ('Nada', 'Nada')
]

# Constantes para 0-2 opciones
CHOICES_0_2 = (
    ("No", "No"),
    ("Si, uno", "Si, uno"),
    ("Si, dos o más", "Si, dos o más")
)

# Constantes para 0-3 opciones
CHOICES_0_3 = (
    ("Ninguna", "Ninguna"),
    ("Una", "Una"),
    ("Dos", "Dos"),
    ("Tres o más", "Tres o más")
)

# Constantes para sí/no/no sé
CHOICES_SI_NO_NOSE = (
    ("No", "No"),
    ("Si", "Si"),
    ("No lo sé", "No lo sé")
)

# Constantes para principal sostén
CHOICES_PRINCIPAL_SOSTEN = (
    ("1. La madre del chico o chica", "1. La madre del chico o chica"),
    ("2. El padre del chico o chica", "2. El padre del chico o chica"),
    ("3. Un abuelo o abuela del chico o chica", "3. Un abuelo o abuela del chico o chica"),
    ("4. Otra persona", "4. Otra persona"),
)