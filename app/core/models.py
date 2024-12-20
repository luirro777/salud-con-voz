from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

CHOICES_NIVEL_EDUCATIVO = (
	("1. No fue a la escuela", "1. No fue a la escuela"),
	("2. Primaria incompleta (comenzó, pero no terminó la escuela primaria)", "2. Primaria incompleta (comenzó, pero no terminó la escuela primaria)"),
	("3. Primaria completa", "3. Primaria completa"),
	("4. Secundaria incompleta (comenzó, pero no terminó la secundaria)", "4. Secundaria incompleta (comenzó, pero no terminó la secundaria)"),
	("5. Secundaria completa", "5. Secundaria completa"),
	("6. Terciario o universitario incompleto (los comenzó, pero no los terminó)a", "6. Terciario o universitario incompleto (los comenzó, pero no los terminó)a"),
	("7. Terciario completa", "7. Terciario completa"),
	("8. Universitario de grado completo o posgrado completo", "8. Universitario de grado completo o posgrado completo")
)


class Tutor(models.Model):
	
	edad = models.IntegerField(verbose_name="Edad: [De la persona que responde]")
	CHOICES_RELACION = {
		'madre': 'Madre',
		'padre': 'Padre',
		'tutor': 'Tutor/a legal',
		'pareja-padre-madre': 'Pareja de la madre o el padre',
		'abuelo': 'Abuela/o',
		'hermano': 'Hermana/o',
		'otro-familiar': 'Otro familiar',
		'otro-no-familiar': 'Otra persona, no familiar',
	}	
	relacion = models.CharField(max_length=100, choices=CHOICES_RELACION, verbose_name="¿Cuál es su relación con el niño/a o adolescente?")
	relacion_otro = models.CharField(max_length=100, verbose_name="¿Cuál?", blank=True, null=True)
	CHOICES_QUIEN_CUIDA = {
		'solo': 'Sí, generalmente sola /solo',
		'con-ayuda': 'Sí, con la ayuda de otra/s persona/s',
		'otra-persona': 'No, generalmente otra/s persona/s se ocupan del chico/a',
		'otra-opcion': '¿Otra opción?',
	}		
	quien_cuida = models.CharField(max_length=100, choices=CHOICES_QUIEN_CUIDA, verbose_name="¿Usted es la persona que se ocupa principalmente del cuidado?")
	quien_cuida_otro = models.CharField(max_length=100, verbose_name="¿Quién/es? Por favor, especifique", blank=True, null=True)
	estudios_alcanzados = models.CharField(max_length=200, choices=CHOICES_NIVEL_EDUCATIVO, verbose_name="¿Cuál es el nivel máximo de estudios finalizado por la madre del niño/a o adolescente?")
	CHOICES_SALUD = {
		'mala': 'Mala',
		'regular': 'Regular',
		'buena': 'Buena',
		'muy-buena': 'Muy buena',
		'excelente': 'Excelente',
	}
	estado_salud = models.CharField(max_length=20, choices=CHOICES_SALUD, verbose_name="Usted diría que SU SALUD es: [De la persona que responde]")
	CHOICES_GENERO = {
		'femenino': 'Femenino',
		'masculino': 'Masculino',
		'no-binario': 'No binario',
		'otro': 'Otro',
	}
	genero = models.CharField(max_length=20, choices=CHOICES_GENERO, verbose_name="Género")
	genero_otro = models.CharField(max_length=20, verbose_name="¿Cuál?", blank=True, null=True)	











class Paciente(models.Model):
	edad = models.IntegerField(verbose_name="Edad: [Del niño/a o adolescente]")
	fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento: [Del niño/a o adolescente]")
	CHOICES_GENERO = {
		'femenino': 'Femenino',
		'masculino': 'Masculino',
		'no-binario': 'No binario',
		'otro': 'Otro',
	}
	genero = models.CharField(max_length=20, choices=CHOICES_GENERO, verbose_name="Género")
	genero_otro = models.CharField(max_length=20, verbose_name="¿Cuál?", blank=True, null=True)
	CHOICES_PROVINCIA = {
			"Ciudad Autónoma de Buenos Aires": "Ciudad Autónoma de Buenos Aires",
			"Buenos Aires": "Buenos Aires",
			"Catamarca": "Catamarca",
			"Córdoba": "Córdoba",
			"Corrientes": "Corrientes",
			"Entre Ríos": "Entre Ríos",
			"Jujuy": "Jujuy",
			"Mendoza": "Mendoza",
			"La Rioja": "La Rioja",
			"Salta": "Salta",
			"San Juan": "San Juan",
			"San Luis": "San Luis",
			"Santa Fe": "Santa Fe",
			"Santiago del Estero": "Santiago del Estero",
			"Tucumán": "Tucumán",
			"Chaco": "Chaco",
			"Chubut": "Chubut",
			"Formosa": "Formosa",
			"Misiones": "Misiones",
			"Neuquén": "Neuquén",
			"La Pampa": "La Pampa",
			"Río Negro": "Río Negro",
			"Santa Cruz": "Santa Cruz",
			"Tierra del Fuego": "Tierra del Fuego",
	}

	provincia = models.CharField(max_length=100, choices=CHOICES_PROVINCIA, verbose_name="Lugar de residencia: [Provincia]")
	ciudad = models.CharField(max_length=100, verbose_name="Lugar de residencia: [Ciudad]")
	CHOICES_COBERTURA = {
		"sistema-publico": "Utiliza el sistema público exclusivamente.",
		"programa-estatal": "Programas o planes estatales de salud",
		"pami": "PAMI",
		"obra-social": "Obra social (por ejemplo: APROSS, OSECAC, UOM, OSPACA, OSPECOM, UOCRA, UPCN, etc.)",
		"prepaga-obra-social": "Prepaga a través de obra social (por ejemplo: GEA, MEDIFE, OSDE, SIPSSA, OMINT, SWISS MEDICAL, etc.)",
		"prepaga-voluntaria": "Prepaga por contratación voluntaria (por ejemplo: GEA, MEDIFE, OSDE, SIPSSA, OMINT, SWISS MEDICAL, etc.)",
		"emergencia-medica": "Emergencia médica (por ejemplo: URG, EMI, etc.)",
		"nsnr": "No sé / No respondo."
	}
	cobertura = models.CharField(max_length=100, choices=CHOICES_COBERTURA, verbose_name="¿Qué tipo de cobertura de salud tiene su hijo/a actualmente?")
	cobertura_cual = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuál?")
	CHOICES_CUD = {
		"no": "No",
		"si": "Si",
		"nsnr": "No sé / No respondo",
	}
	certificado_discapacidad = models.CharField(max_length=100, choices=CHOICES_CUD, verbose_name="¿Su hijo tiene Certificado Único de Discapacidad (CUD)?")	
	CHOICES_MOVIMIENTO = {
		1: 'Tiene dificultad para mantenerse sentado y para poder controlar la cabeza y el tronco en cualquier posición.',
		2: 'Puede mantenerse sentado con algún soporte en pelvis o en tronco, pero no estar de pie, ni caminar sin gran ayuda.',
		3: 'Es capaz de mantenerse de pie por sí mismo y de caminar, sólo si usa alguna ayuda para la marcha (como un andador, muletas, bastones, etc.)',
		4: 'Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamano para subir y bajar escaleras.',
		5: 'Puede caminar sin ayudas para la marcha y subir y bajar escaleras sin necesidad de apoyarse en el pasamano.',
	}
	movimiento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=CHOICES_MOVIMIENTO, verbose_name="Por favor, seleccione la opción que mejor describa la capacidad de movimiento del niño/a o adolescente:")



CHOICES_SENTIMIENTOS = {
	1:'1 - Muy Desconforme',
	2:'2',
	3:'3',
	4:'4',
	5:'5',
	6:'6',
	7:'7',
	8:'8',
	9:'9 - Muy Conforme',
	}

CHOICES_DOLOR = {
	1:'1 - Nada de dolor',
	2:'2',
	3:'3',
	4:'4',
	5:'5',
	6:'6',
	7:'7',
	8:'8',
	9:'9 - Mucho dolor',
	}

CHOICES_MOLESTIA = {
	1:'1 - Nada molesto',
	2:'2',
	3:'3',
	4:'4',
	5:'5',
	6:'6',
	7:'7',
	8:'8',
	9:'9 - Muy molesto',
	}


class Calculadora:

	MAPPER = {
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

	def promedio(self):
		suma = 0
		fields = self._meta.get_fields()
		for field in fields:
			if isinstance(field, models.IntegerField):
				field_name = field.name
				suma += self.MAPPER[getattr(self, field_name)]
		
		return suma/len(fields)	
	

class Sentimientos(models.Model, Calculadora):
	hacer_cosas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para hacer las cosas que quiere hacer?") 
	uno_mismo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a él/ella mismo/a?")
	motivacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su motivación?")
	oportunidades = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a sus oportunidades en la vida?")
	aspecto_fisico = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su aspecto físico?")

	
	

class Relaciones(models.Model, Calculadora):
	con_gente = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con la gente en general?") 
	otros_chichos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con otros chicos fuera de la escuela o el colegio (que no son sus amigos de la escuela/colegio)?")
	con_adultos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con los adultos?")
	con_amigos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a juntarse con amigos/as?")
	aceptacion_otros_chicos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por otros chicos fuera de la escuela o el colegio (que no son sus amigos de la escuela/colegio)?")
	aceptacion_adultos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por los adultos?")
	aceptacion_gente = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado por la gente en general?")
	cosas_nuevas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a la forma en que intenta probar cosas nuevas?")
	comunicacion_conocidos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a la forma en que se comunica con la gente que conoce bien?")
	comunicacion_extranios = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a la forma en que se comunica con la gente que NO conoce bien?")
	comunicacion_otros_con_el = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a la forma en que otra gente se comunica con su hijo/a?")
	comunicacion_tecnologia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a la forma en que se comunica con la gente utilizando tecnología? (por ejemplo, mensajes de texto, internet)?")

class Familia(models.Model, Calculadora):
	apoyo_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a el apoyo que tiene de su familia?")
	viaje_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a salir de viaje con la familia?") 
	aceptacion_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por su familia?")

class Participacion(models.Model, Calculadora):
	recreativas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en actividades recreativas y de tiempo libre?")
	deportivas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su habilidad para participar en actividades deportivas? (Esta pregunta refiere a cómo se siente su hijo/a acerca de su habilidad para hacer deporte, no si puede hacerlo o no)") 
	eventos_sociales = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en eventos sociales fuera de la escuela o colegio?")  
	en_su_comunidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en su comunidad?")

class Escuela(models.Model, Calculadora):
	otros_chicos_escuela = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con otros chicos en la escuela o colegio?")
	como_lo_integran= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo otros alumnos lo/la integran en la escuela o colegio?") 
	profesores = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con sus maestros, profesores y/o asistentes?")  
	otros_alumnos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por otros alumnos en la escuela o colegio?")
	otros_docentes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por el personal y los docentes de su escuela o colegio?")
	mismo_trato = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a ser tratado/a de la misma manera que los demás en la escuela o colegio?")
	participacion_colegio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en la escuela o colegio?")

class Salud(models.Model, Calculadora):
	hacer_cosas_solo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a hacer cosas solo/a, sin compañía?")
	movilidad= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su forma de trasladarse de un lado a otro? (es decir, su movilidad)?") 
	independencia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a poder hacer cosas solo/a sin depender de otros?")  
	moverse_dentro_barrio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para moverse dentro de su barrio?")
	transporte = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para ir de un lugar a otro (ej. transporte)?")
	brazos_y_manos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su forma de usar sus brazos y sus manos?")
	piernas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su forma de usar sus piernas?")
	vestirse = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para vestirse sólo/a?")
	beber = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para beber sin ayuda?")
	ir_al_banio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para ir al baño sin ayuda?")

class Dolor(models.Model, Calculadora):
	salud_gral = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su salud en general?")
	suenio= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo duerme?") 
	cuanto_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_DOLOR, verbose_name="¿Cuánto dolor siente su hijo/a?")  
	nivel_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a el nivel de dolor que siente?")
	nivel_incomodidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a el nivel de incomodidad que siente?")
	como_afecta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a la forma en que los dolores le afectan en su vida?")
	impedimentos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a la forma en que el dolor le impide ser él/ella mismo/a?")
	no_disfrutar_dia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a como el dolor no le permite pasarlo bien todos los días?")

class Servicios(models.Model, Calculadora):
	acceso_tratamiento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso de su hijo/a al tratamiento?")
	acceso_terapia= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso de su hijo/a a terapia (por ejemplo: fisioterapia, fonoaudiología, terapia ocupacional)?") 
	acceso_atencion_medica= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a atención médica o quirúrgica especializada?") 
	acceso_pediatria= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a atención de pediatría o medicina general?") 
	acceso_ayuda_aprendizaje= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a ayuda adicional de aprendizaje dentro de la escuela o colegio?") 



CHOICES_FINALES = (
	('Nunca' , 'Nunca'),
	('Casi Nunca', 'Casi Nunca'),
	('Algunas Veces', 'Algunas Veces'),
	('Casi Siempre', 'Casi Siempre'),
	('Siempre', 'Siempre')
)

CHOICES_SI_NO = {
		"No":"No" , 
		"Si":"Si"
	}
CHOICES_INTENSIDAD = { 
	('Nada', 'Nada'),
	('Un poco', 'Un poco'),
	('Moderadamente','Moderadamente'),
	('Mucho','Mucho'),
	('Muchísimo','Muchísimo')
}
CHOICES_0_2 = (
	("No", "No"),
	("Si, uno", "Si, uno"),
	("Si, dos o más", "Si, dos o más")
)
CHOICES_0_3 = (
	("Ninguna", "Ninguna"),
	("Una", "Una"),
	("Dos", "Dos"),
	("Tres o más", "Tres o más")
)
CHOICES_SI_NO_NOSE = (
	("No" , "No" ),
	("Si" , "Si" ),
	("No lo sé", "No lo sé")
)
CHOICES_PRINCIPAL_SOSTEN = (
	("1. La madre del chico o chica", "1. La madre del chico o chica"),
	("2. El padre del chico o chica", "2. El padre del chico o chica"),
	("3. Un abuelo o abuela del chico o chica", "3. Un abuelo o abuela del chico o chica"),
	("4. Otra persona", "4. Otra persona"),
)

class SaludUltimaSemana(models.Model):
	frustra = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a se frustra por no poder seguir el ritmo de otros chicos/as?")
	correr= models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le gustaría poder correr como los demás chicos/as?") 
	nadar = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le gustaría poder nadar como los demás chicos/as?")  
	vestirse = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta tardar mucho en vestirse?")
	inteligencia = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a siente que las personas piensan que es menos inteligente de lo que realmente es?")
	edificios = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a tiene problemas para entrar y salir de los edificios?")
	piernas = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="Aunque su hijo/a no pueda mover las piernas muy bien ¿puede hacer la mayoría de las cosas?")
	caminar = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para caminar sin ayuda?")
	caminar_2 = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta no poder caminar sin ayuda?")
	bañarse = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para vestirse o bañarse?")
	bañarse_2 = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta que lo/a tenga que vestir y bañar otra persona?")
	ir_baño = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para ir al baño solo/a?")
	ir_baño_2 = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta que lo/a tengan que ayudar para ir al baño?")
	comunicarse = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para comunicarse?")
	comunicarse_2 = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a se puede comunicar tan bien como quiere?")
	hablar = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para hablar?")
	hablar_2 = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta no poder hablar tan bien como los demás chicos/as?")

class SaludUltimaSemana2(models.Model):
	fisicamente = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió bien y físicamente en forma?")
	energia= models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió lleno/a de energía?") 
	tristeza = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió triste?")  
	soledad = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió solo/a?")
	tiempo_libre = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a tuvo suficiente tiempo para él/ella?")
	cosas_queria = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a hizo las cosas que quería hacer en su tiempo libre?")
	justicia = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿Los padres del chico/a fueron justos con él/ella?")
	diversion = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se divirtió con sus amigos/as?")
	colegio = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿Al chico/a le fue bien en la escuela o en el colegio?")
	atencion = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a pudo prestar atención en clase?")

class Hogar(models.Model):
	dormitorio_propio = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿El chico o chica cuenta con un dormitorio para el/ella solo/a?")
	autos = models.CharField(max_length=100, choices=CHOICES_0_2, verbose_name="¿La familia tiene auto o camioneta propios?") 
	computadoras = models.CharField(max_length=100, choices=CHOICES_0_3, verbose_name="¿Cuántas computadoras, notebooks o tablets en funcionamiento tiene en total la familia? No incluya videojuegos y teléfonos con acceso a internet.")  
	duchas = models.CharField(max_length=100, choices=CHOICES_0_3, verbose_name="¿Cuántos baños con ducha (o bañera) hay en su casa?")
	lavaplatos = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su familia tiene una máquina lavaplatos en casa?")
	tareas_hogar = models.CharField(max_length=100, choices=CHOICES_SI_NO_NOSE, verbose_name="¿Alguna persona que no sea de su familia va a su casa a hacer tareas del hogar? Tareas de servicio doméstico como limpiar, lavar, planchar, etc.")
	vacaciones = models.CharField(max_length=100, choices=CHOICES_0_3, verbose_name="Durante los últimos 12 meses, ¿cuántas veces salió de vacaciones con su familia a algún lugar dónde se quedaron más de un día?")
	nivel_estudio = models.CharField(max_length=100, choices=CHOICES_NIVEL_EDUCATIVO, verbose_name="¿Cuál es el nivel máximo de estudios finalizado por la madre del chico o chica?")
	sosten_economico = models.CharField(max_length=100, choices=CHOICES_PRINCIPAL_SOSTEN, verbose_name="¿Quién es el principal sostén económico del hogar donde vive el chico o chica?")
	otros=  models.CharField(max_length=100, blank=True, null=True, verbose_name="Si respondió: otra persona, por favor indique ¿Quién?")
	nivel_estudio_2 = models.CharField(max_length=100, choices=CHOICES_NIVEL_EDUCATIVO, verbose_name="¿Cuál es el máximo nivel de estudios que alcanzó esta persona (principal sostén económico del hogar)?")






class Cpqol(models.Model):
	creacion = models.DateTimeField('creacion',auto_now_add=True)
	user=models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
	codigo=models.CharField(max_length=100, blank=True, null=True)
	tutor=models.ForeignKey(Tutor, blank=True, null=True, on_delete=models.PROTECT)
	paciente=models.ForeignKey(Paciente, blank=True, null=True, on_delete=models.PROTECT)
	sentimientos=models.ForeignKey(Sentimientos, blank=True, null=True, on_delete=models.PROTECT)
	relaciones=models.ForeignKey(Relaciones, blank=True, null=True, on_delete=models.PROTECT)
	familia=models.ForeignKey(Familia, blank=True, null=True, on_delete=models.PROTECT)
	participacion=models.ForeignKey(Participacion, blank=True, null=True, on_delete=models.PROTECT)
	escuela=models.ForeignKey(Escuela, blank=True, null=True, on_delete=models.PROTECT)
	salud=models.ForeignKey(Salud, blank=True, null=True, on_delete=models.PROTECT)
	dolor=models.ForeignKey(Dolor, blank=True, null=True, on_delete=models.PROTECT)
	servicios=models.ForeignKey(Servicios, blank=True, null=True, on_delete=models.PROTECT)
	salud_ultima_semana=models.ForeignKey(SaludUltimaSemana, blank=True, null=True, on_delete=models.PROTECT)
	salud_ultima_semana_2=models.ForeignKey(SaludUltimaSemana2, blank=True, null=True, on_delete=models.PROTECT)
	hogar=models.ForeignKey(Hogar, blank=True, null=True, on_delete=models.PROTECT)
	
	

	class Meta:
		verbose_name_plural = "Lista De Formularios"

	@property
	def current_seccion(self):
		if self.hogar: return 14
		if not self.tutor: return 2 
		if not self.paciente: return 3
		if not self.sentimientos: return 4
		if not self.relaciones: return 5
		if not self.familia: return 6
		if not self.participacion: return 7
		if not self.escuela: return 8
		if not self.salud: return 9
		if not self.dolor: return 10 
		if not self.servicios: return 11
		if not self.salud_ultima_semana: return 12
		if not self.salud_ultima_semana2: return 13
		return 0
	
	@property
	def confirmado(self):
		return self.hogar != None

	@property
	def resultados(self):
		return {
			'Bienestar emocional': self.sentimientos.promedio(),
			'Bienestar y aceptación social': self.relaciones.promedio(),
			'Relaciones en la familia': self.familia.promedio(),
			'Participación': self.participacion.promedio(),
			'Entorno escolar': self.escuela.promedio(),
			'Autonomía': self.salud.promedio(),
			'Dolor': self.dolor.promedio(),
			'Acceso a Servicios': self.servicios.promedio()
		}