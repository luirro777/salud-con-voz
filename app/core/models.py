from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import (
    CHOICES_NIVEL_EDUCATIVO, CHOICES_PROFESION, CHOICES_TIPO_CENTRO,
    CHOICES_PERSONA_OCUPA, CHOICES_GENERO, CHOICES_NIVEL,
    CHOICES_SENTIMIENTOS, CHOICES_DOLOR, CHOICES_MOLESTIA,
    CHOICES_FINALES, CHOICES_FINALES_2, CHOICES_SI_NO,
    CHOICES_INTENSIDAD, CHOICES_INTENSIDAD_2, CHOICES_0_2,
    CHOICES_0_3, CHOICES_SI_NO_NOSE, CHOICES_PRINCIPAL_SOSTEN
)


'''
Para profesionales
'''
class Profesional(models.Model):
	profesion = models.CharField(
    	max_length=100,
    	choices=CHOICES_PROFESION,
    	verbose_name="Por favor, marque la profesión que mejor le describa"
	)
	provincia_atencion = models.CharField(
		verbose_name="Por favor, consigne la provincia en la que atiende al niño, niña, adolescente o jóven",
		max_length=100
	)
	ciudad_atencion = models.CharField(
		verbose_name="Ciudad o localidad donde atiende al NNAJ"
	)
	tipo_centro = models.CharField(
		max_length=100,
		choices=CHOICES_TIPO_CENTRO,
		verbose_name="Por favor, indique el tipo de centro o servicio de salud en el que trabaja:"
	)
	centro_salud = models.CharField(
		max_length=100,
		verbose_name="Por favor, consigne el nombre del centro o servicio de salud en el que trabaja (si es consultorio particular escriba 'consultorio particular'):"
	)
	# Especialidad (en caso de haber seleccionado medico especialista)
	especialidad = models.CharField(
		max_length=255,
		verbose_name="Qué especialidad?",
		blank=True,
		null=True
	)	
	# En caso de haber seleccionado "otra"
	profesion_otra = models.CharField(
		max_length=255,
		verbose_name="Cuál?",
		blank=True,
		null=True
	)
	# En caso de seleccionar "otro" en tipo de centro
	tipo_centro_otro = models.CharField(
		max_length=255,
		verbose_name="Cuál?",
		blank=True,
		null=True
	)
	
class Contexto(models.Model):
	persona_ocupa = models.CharField(
    	max_length=100,
    	choices=CHOICES_PERSONA_OCUPA,
    	verbose_name="¿Quién es la persona que se ocupa principalmente del cuidado del niño, niña adolescente o jóven?"
	)
	max_estudios = models.CharField(
		max_length=100,
		choices=CHOICES_NIVEL_EDUCATIVO,
		verbose_name="¿Cuál es el nivel máximo de estudios finalizado por la madre o cuidador/a del niño/a, adolescente o jóven?"
	)
	edad = models.PositiveIntegerField(
		validators=[
			MaxValueValidator(18, "La edad no puede superar los 18 años")
		],
		verbose_name="Edad del niño, niña, adolescente o jóven:"
	)
	genero = models.CharField(
		max_length=100,
		choices= CHOICES_GENERO,
		verbose_name="Género del niño, niña, adolescente o jóven"
	)

class DatosClinicos(models.Model):
	gmfcs = models.CharField(
		max_length=100,
		choices=CHOICES_NIVEL,
		verbose_name="Sistema de la Clasificación de la Función Motora Gruesa (GMFCS)"
	)
	macs = models.CharField(
		max_length=100,
		choices=CHOICES_NIVEL,
		verbose_name="Sistema de Clasificación de la Habilidad Manual (MACS)"
	)
	cfcs = models.CharField(
		max_length=100,
		choices=CHOICES_NIVEL,
		verbose_name="Sistema de Clasificación de Comunicación Funcional (CFCS)"
	)
	edacs = models.CharField(
		max_length=100,
		choices=CHOICES_NIVEL,
		verbose_name="Sistema de Clasificación para la capacidad de Comer y Beber (EDACS)"
	)


# Este es compartido por profesionales y familiares
class Finalizacion(models.Model):
	correo = models.EmailField(
        max_length=254,
        blank=True, 
        null=True, 
        default='correo@ejemplo.com' # Valor por defecto para la base de datos
    )

	def __str__(self):
		return f"Finalización: {self.correo if self.correo else 'No proporcionado'}"

'''
Para familiares
'''
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
	genero = models.CharField(max_length=20, choices=CHOICES_GENERO, verbose_name="Género [de la persona que responde]")
	genero_otro = models.CharField(max_length=20, verbose_name="¿Cuál?", blank=True, null=True)

	def __str__(self):
		return f"Tutor: {self.relacion} - Edad: {self.edad}"	


class Paciente(models.Model):
	edad = models.IntegerField(verbose_name="Edad: [Del niño/a o adolescente]")
	fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento: [Del niño/a o adolescente]")
	CHOICES_GENERO = {
		'femenino': 'Femenino',
		'masculino': 'Masculino',
		'no-binario': 'No binario',
		'otro': 'Otro',
	}
	genero = models.CharField(max_length=20, choices=CHOICES_GENERO, verbose_name="Género [Del niño/a o adolescente]")
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
		"sistema_publico": "Utiliza el sistema público exclusivamente.",
		"programa_estatal": "Programas o planes estatales de salud",
		"pami": "PAMI",
		"obra_social": "Obra social (por ejemplo: APROSS, OSECAC, UOM, OSPACA, OSPECOM, UOCRA, UPCN, etc.)",
		"prepaga_obra_social": "Prepaga a través de obra social (por ejemplo: GEA, MEDIFE, OSDE, SIPSSA, OMINT, SWISS MEDICAL, etc.)",
		"prepaga_voluntaria": "Prepaga por contratación voluntaria (por ejemplo: GEA, MEDIFE, OSDE, SIPSSA, OMINT, SWISS MEDICAL, etc.)",
		"emergencia_medica": "Emergencia médica (por ejemplo: URG, EMI, etc.)",
		"nsnr": "No sé / No respondo."
	}
	#cobertura = models.CharField(max_length=100, choices=CHOICES_COBERTURA, verbose_name="¿Qué tipo de cobertura de salud tiene su hijo/a actualmente?")
	cobertura = models.JSONField(verbose_name="¿Qué tipo de cobertura de salud tiene su hijo/a actualmente?", blank=True, null=True)
	cobertura_cual = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuál? (Responder solo en caso de haber seleccionado 'obra social', 'prepaga a través de obra social' o 'prepaga por contratación voluntaria')", default="---")
	CHOICES_CUD = {
		"no": "No",
		"si": "Si",
		"nsnr": "No sé / No respondo",
	}
	certificado_discapacidad = models.CharField(max_length=100, choices=CHOICES_CUD, verbose_name="¿Su hijo tiene Certificado Único de Discapacidad (CUD)?")

	def __str__(self):
		return f"Paciente: {self.edad} años - Género: {self.genero} - Provincia: {self.provincia}"
	
	def get_cobertura_display(self):
		"""
		Devuelve una representación legible de las coberturas seleccionadas
		"""
		if not self.cobertura:
			return "No especificado"
        
		try:
			if isinstance(self.cobertura, list):
				display_values = []
				for item in self.cobertura:
					display = self.CHOICES_COBERTURA.get(item, item)
					display_values.append(display)
				return ", ".join(display_values)
			elif isinstance(self.cobertura, str):
				return self.CHOICES_COBERTURA.get(self.cobertura, self.cobertura)
			else:
				return str(self.cobertura)
		except (AttributeError, TypeError):
			return str(self.cobertura)
	

class Movimiento(models.Model):
    movimiento = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)],    
    verbose_name="Por favor lea las 5 posibles situaciones descritas antes de contestar. Seleccione sólo una opción, marcando el casillero. Elija la que mejor describa de manera general, la capacidad de su hijo/a para moverse.",     
    default=1, # Se mantiene el default para la base de datos, aunque el form lo sobrescriba
    null=False,     
    blank=False, 
	)
    

    def __str__(self):
        return f"Movimiento: {self.movimiento}"	

class Sentimientos(models.Model):
	
	hacer_cosas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para hacer las cosas que quiere hacer?") 
	uno_mismo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a él/ella mismo/a?")
	motivacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su motivación?")
	oportunidades = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a sus oportunidades en la vida?")
	aspecto_fisico = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su aspecto físico?")
	promedio = models.FloatField(blank=True, null=True, default=0.0)    
    
	def __str__(self):
		return f"Sentimientos: {self.promedio}"     
	

class Relaciones(models.Model):
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
	promedio = models.FloatField(default=0.0)

	def __str__(self):
		return f"Relaciones: {self.promedio}"

class Familia(models.Model):
	apoyo_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a el apoyo que tiene de su familia?")
	viaje_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a salir de viaje con la familia?") 
	aceptacion_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por su familia?")
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Familia: {self.promedio}"

class Participacion(models.Model):
	recreativas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en actividades recreativas y de tiempo libre?")
	deportivas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su habilidad para participar en actividades deportivas? (Esta pregunta refiere a cómo se siente su hijo/a acerca de su habilidad para hacer deporte, no si puede hacerlo o no)") 
	eventos_sociales = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en eventos sociales fuera de la escuela o colegio?")  
	en_su_comunidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en su comunidad?")
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Participacion: {self.promedio}"

class Escuela(models.Model):
	otros_chicos_escuela = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con otros chicos en la escuela o colegio?")
	como_lo_integran= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo otros alumnos lo/la integran en la escuela o colegio?") 
	profesores = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo se lleva con sus maestros, profesores y/o asistentes?")  
	otros_alumnos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por otros alumnos en la escuela o colegio?")
	otros_docentes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo es aceptado/a por el personal y los docentes de su escuela o colegio?")
	mismo_trato = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a ser tratado/a de la misma manera que los demás en la escuela o colegio?")
	participacion_colegio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su capacidad para participar en la escuela o colegio?")
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Escuela: {self.promedio}"

class Salud(models.Model):
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
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Salud: {self.promedio}"

class Dolor(models.Model):
	salud_gral = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a su salud en general?")
	suenio= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo piensa que su hijo/a se siente con respecto a cómo duerme?") 
	cuanto_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_DOLOR, verbose_name="¿Cuánto dolor siente su hijo/a?")  
	nivel_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a el nivel de dolor que siente?")
	nivel_incomodidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a el nivel de incomodidad que siente?")
	como_afecta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a la forma en que los dolores le afectan en su vida?")
	impedimentos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a la forma en que el dolor le impide ser él/ella mismo/a?")
	no_disfrutar_dia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA, verbose_name="¿Cómo se siente su hijo/a con respecto a como el dolor no le permite pasarlo bien todos los días?")
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Dolor: {self.promedio}"

class Servicios(models.Model):
	acceso_tratamiento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso de su hijo/a al tratamiento?")
	acceso_terapia= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso de su hijo/a a terapia (por ejemplo: fisioterapia, fonoaudiología, terapia ocupacional)?") 
	acceso_atencion_medica= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a atención médica o quirúrgica especializada?") 
	acceso_pediatria= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a atención de pediatría o medicina general?") 
	acceso_ayuda_aprendizaje= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS, verbose_name="¿Cómo se siente USTED con respecto a el acceso a ayuda adicional de aprendizaje dentro de la escuela o colegio?") 
	promedio = models.FloatField(blank=True, null=True, default=0.0)

	def __str__(self):
		return f"Servicios: {self.promedio}"


class SaludUltimaSemana(models.Model):
	frustra = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a se frustra por no poder seguir el ritmo de otros chicos/as?")
	correr= models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le gustaría poder correr como los demás chicos/as?") 
	nadar = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le gustaría poder nadar como los demás chicos/as?")  
	vestirse = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿A su hijo/a le molesta tardar mucho en vestirse?")
	inteligencia = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a siente que las personas piensan que es menos inteligente de lo que realmente es?")
	edificios = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="¿Su hijo/a tiene problemas para entrar y salir de los edificios?")
	piernas = models.CharField(max_length=100, choices=CHOICES_FINALES, verbose_name="Aunque su hijo/a no pueda mover las piernas muy bien ¿puede hacer la mayoría de las cosas?")
	#caminar = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para caminar sin ayuda?")
	caminar_2 = models.CharField(max_length=100, choices=CHOICES_FINALES_2, verbose_name="¿A su hijo/a le molesta no poder caminar sin ayuda?")
	#bañarse = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para vestirse o bañarse?")
	bañarse_2 = models.CharField(max_length=100, choices=CHOICES_FINALES_2, verbose_name="¿A su hijo/a le molesta que lo/a tenga que vestir y bañar otra persona?")
	#ir_baño = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para ir al baño solo/a?")
	ir_baño_2 = models.CharField(max_length=100, choices=CHOICES_FINALES_2, verbose_name="¿A su hijo/a le molesta que lo/a tengan que ayudar para ir al baño?")
	#comunicarse = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para comunicarse?")
	comunicarse_2 = models.CharField(max_length=100, choices=CHOICES_FINALES_2, verbose_name="¿Su hijo/a se puede comunicar tan bien como quiere?")
	#hablar = models.CharField(max_length=100, choices=CHOICES_SI_NO, verbose_name="¿Su hijo/a tiene problemas para hablar?")
	hablar_2 = models.CharField(max_length=100, choices=CHOICES_FINALES_2, verbose_name="¿A su hijo/a le molesta no poder hablar tan bien como los demás chicos/as?")

class SaludUltimaSemana2(models.Model):
	fisicamente = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD_2, verbose_name="¿El chico/a se sintió bien y físicamente en forma?")
	energia= models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió lleno/a de energía?") 
	tristeza = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió triste?")  
	soledad = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se sintió solo/a?")
	tiempo_libre = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a tuvo suficiente tiempo para él/ella?")
	cosas_queria = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a hizo las cosas que quería hacer en su tiempo libre?")
	justicia = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿Los padres del chico/a fueron justos con él/ella?")
	diversion = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD, verbose_name="¿El chico/a se divirtió con sus amigos/as?")
	colegio = models.CharField(max_length=100, choices=CHOICES_INTENSIDAD_2, verbose_name="¿Al chico/a le fue bien en la escuela o en el colegio?")
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
	movimiento=models.ForeignKey(Movimiento, blank=True, null=True, on_delete=models.PROTECT)
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
	correo = models.ForeignKey(Finalizacion, blank=True, null=True, on_delete=models.PROTECT)
	completado = models.BooleanField("Completado",default=False)	
	

	class Meta:
		verbose_name_plural = "Lista De Formularios"
	
	@property
	def current_seccion(self):
		# Verificar las secciones en orden
		if not self.tutor: 
			return 2
		if not self.paciente: 
			return 3
		if not self.movimiento: 
			return 4  
		if not self.sentimientos: 
			return 5
		if not self.relaciones: 
			return 6
		if not self.familia: 
			return 7  
		if not self.participacion: 
			return 8
		if not self.escuela: 
			return 9
		if not self.salud: 
			return 10
		if not self.dolor: 
			return 11
		if not self.servicios: 
			return 12
		if not self.salud_ultima_semana: 
			return 13
		if not self.salud_ultima_semana_2: 
			return 14
		if not self.hogar: 
			return 15
		if not self.correo: 
			return 16
		return 17  # Todas las secciones completadas

	
	@property
	def confirmado(self):
		return self.completado

	@property
	def resultados(self):
		return {
			'Bienestar emocional': self.sentimientos.promedio if self.sentimientos else 0,
			'Bienestar y aceptación social': self.relaciones.promedio if self.relaciones else 0,
			'Relaciones en la familia': self.familia.promedio if self.familia else 0,
			'Participación': self.participacion.promedio if self.participacion else 0,
			'Entorno escolar': self.escuela.promedio if self.escuela else 0,
			'Autonomía': self.salud.promedio if self.salud else 0,
			'Dolor': self.dolor.promedio if self.dolor else 0,
			'Acceso a Servicios': self.servicios.promedio if self.servicios else 0
		}
	
	def estado_secciones(self):
		"""Método para diagnóstico que muestra el estado de todas las secciones"""
		return {
			'tutor': self.tutor is not None,
			'paciente': self.paciente is not None,
			'movimiento': self.movimiento is not None,
			'sentimientos': self.sentimientos is not None,
			'relaciones': self.relaciones is not None,
			'familia': self.familia is not None,
			'participacion': self.participacion is not None,
			'escuela': self.escuela is not None,
			'salud': self.salud is not None,
			'dolor': self.dolor is not None,
			'servicios': self.servicios is not None,
			'salud_ultima_semana': self.salud_ultima_semana is not None,
			'salud_ultima_semana_2': self.salud_ultima_semana_2 is not None,
			'hogar': self.hogar is not None,
			'correo': self.correo is not None,
		}
	
	def __str__(self):
		return f"CPQOL {self.codigo} - {self.user} - {'Completado' if self.completado else 'En progreso'}"
    
	def informacion_completa(self):
		"""Devuelve toda la información del cuestionario en formato de texto"""
		if not self.pk:
			return "Cuestionario no guardado aún"

		info = []

		# Información del Tutor
		if self.tutor:
			info.append("Tutor")
			info.append(f"Edad: {self.tutor.edad}")
			info.append(f"Relación: {self.tutor.get_relacion_display()}")
			if self.tutor.relacion_otro:
				info.append(f"Relación (otro): {self.tutor.relacion_otro}")
			info.append(f"¿Quién cuida?: {self.tutor.get_quien_cuida_display()}")
			if self.tutor.quien_cuida_otro:
				info.append(f"¿Quién cuida? (otro): {self.tutor.quien_cuida_otro}")			
			info.append(f"Estado de salud: {self.tutor.get_estado_salud_display()}")
			info.append(f"Género: {self.tutor.get_genero_display()}")
			if self.tutor.genero_otro:
				info.append(f"Género (otro): {self.tutor.genero_otro}")
			info.append("")
        
        # Información del Paciente
		if self.paciente:
			info.append("Paciente")
			info.append(f"Edad: {self.paciente.edad if self.paciente.edad else 'No proporcionado'}")
			info.append(f"Fecha de nacimiento: {self.paciente.fecha_nacimiento if self.paciente.fecha_nacimiento else 'No proporcionado'}")

			# Género
			genero_display = self.paciente.get_genero_display() if self.paciente.genero else 'No proporcionado'
			info.append(f"Género: {genero_display}")
			if self.paciente.genero_otro:
				info.append(f"Género (otro): {self.paciente.genero_otro}")

			# Provincia y ciudad
			provincia_display = self.paciente.get_provincia_display() if self.paciente.provincia else 'No proporcionado'
			info.append(f"Provincia: {provincia_display}")
			info.append(f"Ciudad: {self.paciente.ciudad if self.paciente.ciudad else 'No proporcionado'}")

			# COBERTURA - USANDO EL NUEVO MÉTODO
			cobertura_display = self.paciente.get_cobertura_display()
			info.append(f"Cobertura de salud: {cobertura_display}")

			# Cobertura cual
			if self.paciente.cobertura_cual and self.paciente.cobertura_cual != "---":
				info.append(f"Cobertura (especifique): {self.paciente.cobertura_cual}")

			# Certificado de discapacidad
			cud_display = self.paciente.get_certificado_discapacidad_display() if self.paciente.certificado_discapacidad else 'No proporcionado'
			info.append(f"Certificado de discapacidad: {cud_display}")
			info.append("")
		
        
        # Información del Movimiento
		if self.movimiento:
			info.append("Sobre la motricidad del niño/a o adolescente")
			info.append(f"Movimiento: {self.movimiento.movimiento}")			
			info.append("")

		# Información de Sentimientos
		if self.sentimientos:
			info.append("Sus sentimientos")
			info.append(f"Hacer cosas: {self.sentimientos.hacer_cosas}")
			info.append(f"Uno mismo: {self.sentimientos.uno_mismo}")
			info.append(f"Motivación: {self.sentimientos.motivacion}")
			info.append(f"Oportunidades: {self.sentimientos.oportunidades}")
			info.append(f"Aspecto físico: {self.sentimientos.aspecto_fisico}")
			info.append(f"Promedio: {self.sentimientos.promedio}")
			info.append("")

		# Información de Relaciones
		if self.relaciones:
			info.append("Relaciones con los demás")
			info.append(f"Con gente: {self.relaciones.con_gente}")
			info.append(f"Otros chicos: {self.relaciones.otros_chichos}")
			info.append(f"Con adultos: {self.relaciones.con_adultos}")
			info.append(f"Con amigos: {self.relaciones.con_amigos}")
			info.append(f"Aceptación otros chicos: {self.relaciones.aceptacion_otros_chicos}")
			info.append(f"Aceptación adultos: {self.relaciones.aceptacion_adultos}")
			info.append(f"Aceptación gente: {self.relaciones.aceptacion_gente}")
			info.append(f"Cosas nuevas: {self.relaciones.cosas_nuevas}")
			info.append(f"Comunicación conocidos: {self.relaciones.comunicacion_conocidos}")
			info.append(f"Comunicación extraños: {self.relaciones.comunicacion_extranios}")
			info.append(f"Comunicación otros con él: {self.relaciones.comunicacion_otros_con_el}")
			info.append(f"Comunicación tecnología: {self.relaciones.comunicacion_tecnologia}")
			info.append(f"Promedio: {self.relaciones.promedio}")
			info.append("")

		# Información de Familia
		if self.familia:
			info.append("Familia")
			info.append(f"Apoyo familia: {self.familia.apoyo_flia}")
			info.append(f"Viaje familia: {self.familia.viaje_flia}")
			info.append(f"Aceptación familia: {self.familia.aceptacion_flia}")
			info.append(f"Promedio: {self.familia.promedio}")
			info.append("")

		# Información de Participación
		if self.participacion:
			info.append("Participación")
			info.append(f"Recreativas: {self.participacion.recreativas}")
			info.append(f"Deportivas: {self.participacion.deportivas}")
			info.append(f"Eventos sociales: {self.participacion.eventos_sociales}")
			info.append(f"En su comunidad: {self.participacion.en_su_comunidad}")
			info.append(f"Promedio: {self.participacion.promedio}")
			info.append("")

		# Información de Escuela
		if self.escuela:
			info.append("Escuela o colegio")
			info.append(f"Otros chicos escuela: {self.escuela.otros_chicos_escuela}")
			info.append(f"Cómo lo integran: {self.escuela.como_lo_integran}")
			info.append(f"Profesores: {self.escuela.profesores}")
			info.append(f"Otros alumnos: {self.escuela.otros_alumnos}")
			info.append(f"Otros docentes: {self.escuela.otros_docentes}")
			info.append(f"Mismo trato: {self.escuela.mismo_trato}")
			info.append(f"Participación colegio: {self.escuela.participacion_colegio}")
			info.append(f"Promedio: {self.escuela.promedio}")
			info.append("")

		# Información de Salud
		if self.salud:
			info.append("Salud")
			info.append(f"Hacer cosas solo: {self.salud.hacer_cosas_solo}")
			info.append(f"Movilidad: {self.salud.movilidad}")
			info.append(f"Independencia: {self.salud.independencia}")
			info.append(f"Moverse dentro barrio: {self.salud.moverse_dentro_barrio}")
			info.append(f"Transporte: {self.salud.transporte}")
			info.append(f"Brazos y manos: {self.salud.brazos_y_manos}")
			info.append(f"Piernas: {self.salud.piernas}")
			info.append(f"Vestirse: {self.salud.vestirse}")
			info.append(f"Beber: {self.salud.beber}")
			info.append(f"Ir al baño: {self.salud.ir_al_banio}")
			info.append(f"Promedio: {self.salud.promedio}")
			info.append("")

		# Información de Dolor
		if self.dolor:
			info.append("Dolor y molestias")
			info.append(f"Salud general: {self.dolor.salud_gral}")
			info.append(f"Sueño: {self.dolor.suenio}")
			info.append(f"Cuánto dolor: {self.dolor.cuanto_dolor}")
			info.append(f"Nivel dolor: {self.dolor.nivel_dolor}")
			info.append(f"Nivel incomodidad: {self.dolor.nivel_incomodidad}")
			info.append(f"Cómo afecta: {self.dolor.como_afecta}")
			info.append(f"Impedimentos: {self.dolor.impedimentos}")
			info.append(f"No disfrutar día: {self.dolor.no_disfrutar_dia}")
			info.append(f"Promedio: {self.dolor.promedio}")
			info.append("")

		# Información de Servicios
		if self.servicios:
			info.append("Acceso a servicios")
			info.append(f"Acceso tratamiento: {self.servicios.acceso_tratamiento}")
			info.append(f"Acceso terapia: {self.servicios.acceso_terapia}")
			info.append(f"Acceso atención médica: {self.servicios.acceso_atencion_medica}")
			info.append(f"Acceso pediatría: {self.servicios.acceso_pediatria}")
			info.append(f"Acceso ayuda aprendizaje: {self.servicios.acceso_ayuda_aprendizaje}")
			info.append(f"Promedio: {self.servicios.promedio}")
			info.append("")

		# Información de SaludUltimaSemana
		if self.salud_ultima_semana:
			info.append("Más preguntas sobre la salud del niño/a o adolescente")
			info.append(f"¿Su hijo/a se frustra por no poder seguir el ritmo de otros chicos/as?: {self.salud_ultima_semana.frustra}")
			info.append(f"¿A su hijo/a le gustaría poder correr como los demás chicos/as? {self.salud_ultima_semana.correr}")
			info.append(f"¿A su hijo/a le gustaría poder nadar como los demás chicos/as?: {self.salud_ultima_semana.nadar}")
			info.append(f"¿A su hijo/a le molesta tardar mucho en vestirse?: {self.salud_ultima_semana.vestirse}")
			info.append(f"¿Su hijo/a siente que las personas piensan que es menos inteligente de lo que realmente es?: {self.salud_ultima_semana.inteligencia}")
			info.append(f"¿Su hijo/a tiene problemas para entrar y salir de los edificios?: {self.salud_ultima_semana.edificios}")
			info.append(f"Aunque su hijo/a no pueda mover las piernas muy bien ¿puede hacer la mayoría de las cosas?: {self.salud_ultima_semana.piernas}")
			info.append(f"¿A su hijo/a le molesta no poder caminar sin ayuda?: {self.salud_ultima_semana.caminar_2}")
			info.append(f"¿A su hijo/a le molesta que lo/a tenga que vestir y bañar otra persona?: {self.salud_ultima_semana.bañarse_2}")
			info.append(f"¿A su hijo/a le molesta que lo/a tengan que ayudar para ir al baño?: {self.salud_ultima_semana.ir_baño_2}")
			info.append(f"¿Su hijo/a se puede comunicar tan bien como quiere?: {self.salud_ultima_semana.comunicarse_2}")
			info.append(f"¿A su hijo/a le molesta no poder hablar tan bien como los demás chicos/as?: {self.salud_ultima_semana.hablar_2}")
			info.append("")

		# Información de SaludUltimaSemana2
		if self.salud_ultima_semana_2:
			info.append("Sobre la salud del chico o chica")
			info.append(f"¿El chico/a se sintió bien y físicamente en forma?: {self.salud_ultima_semana_2.fisicamente}")
			info.append(f"¿El chico/a se sintió lleno/a de energía?: {self.salud_ultima_semana_2.energia}")
			info.append(f"¿El chico/a se sintió triste? {self.salud_ultima_semana_2.tristeza}")
			info.append(f"¿El chico/a se sintió solo/a?: {self.salud_ultima_semana_2.soledad}")
			info.append(f"¿El chico/a tuvo suficiente tiempo para él/ella?: {self.salud_ultima_semana_2.tiempo_libre}")
			info.append(f"¿El chico/a hizo las cosas que quería hacer en su tiempo libre?: {self.salud_ultima_semana_2.cosas_queria}")
			info.append(f"¿Los padres del chico/a fueron justos con él/ella?: {self.salud_ultima_semana_2.justicia}")
			info.append(f"¿El chico/a se divirtió con sus amigos/as? {self.salud_ultima_semana_2.diversion}")
			info.append(f"¿Al chico/a le fue bien en la escuela o en el colegio? {self.salud_ultima_semana_2.colegio}")
			info.append(f"¿El chico/a pudo prestar atención en clase? {self.salud_ultima_semana_2.atencion}")
			info.append("")

		# Información de Hogar
		if self.hogar:
			info.append("Caracterísiticas del hogar")
			info.append(f"Dormitorio propio: {self.hogar.dormitorio_propio}")
			info.append(f"Autos: {self.hogar.autos}")
			info.append(f"Computadoras: {self.hogar.computadoras}")
			info.append(f"Duchas: {self.hogar.duchas}")
			info.append(f"Lavaplatos: {self.hogar.lavaplatos}")
			info.append(f"Tareas hogar: {self.hogar.tareas_hogar}")
			info.append(f"Vacaciones: {self.hogar.vacaciones}")
			info.append(f"Nivel estudio: {self.hogar.nivel_estudio}")
			info.append(f"Sosten económico: {self.hogar.sosten_economico}")
			info.append(f"Otros: {self.hogar.otros}")
			info.append(f"Nivel estudio 2: {self.hogar.nivel_estudio_2}")
			info.append("")

		# Información de Finalización (correo)
		if self.correo:
			info.append("Finalización")
			info.append(f"Correo: {self.correo.correo}")
			info.append("")

		return "\n".join(info)
    
	informacion_completa.short_description = "Información Completa del Cuestionario"
	
class CpqolProfesional(models.Model):
	creacion = models.DateTimeField('creacion',auto_now_add=True)
	user=models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
	codigo=models.CharField(max_length=100, blank=True, null=True)
	profesional = models.ForeignKey(Profesional, blank=True, null=True, on_delete=models.PROTECT)
	contexto = models.ForeignKey(Contexto, blank=True, null=True, on_delete=models.PROTECT)
	datos_clinicos = models.ForeignKey(DatosClinicos, blank=True, null=True, on_delete=models.PROTECT)
	correo = models.ForeignKey(Finalizacion, blank=True, null=True, on_delete=models.PROTECT)
	completado = models.BooleanField("Completado",default=False)	

	class Meta:
		verbose_name_plural = "Lista De Formularios (Profesionales)"

	@property
	def confirmado(self):
		return self.completado

	@property
	def current_seccion(self):
		if not self.profesional: return 2
		if not self.contexto: return 3
		if not self.datos_clinicos: return 4
		if not self.correo: return 5
		return 0
	