from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

class Tutor(models.Model):
	
	edad = models.IntegerField(verbose_name="Edad: [De la persona que responde]")
	relacion = models.CharField(max_length=50, verbose_name="¿Cuál es su relación con el niño/a o adolescente?")
	quien_cuida = models.CharField(max_length=100, verbose_name="¿Usted es la persona que se ocupa principalmente del cuidado?")
	estudios_alcanzados = models.CharField(max_length=100, verbose_name="¿Cuál es el nivel máximo de estudios finalizado por la madre del niño/a o adolescente?")
	CHOICES_SALUD = {
		'mala': 'Mala',
		'regular': 'Regular',
		'buena': 'Buena',
		'muy-buena': 'Muy buena',
		'excelente': 'Excelente',
	}
	estado_salud = models.CharField(max_length=20, choices=CHOICES_SALUD, verbose_name="Usted diría que SU SALUD es: [De la persona que responde]")

class Paciente(models.Model):
	edad = models.IntegerField(blank=True, null=True, verbose_name="Edad: [Del niño/a o adolescente]")
	CHOICES_GENERO = {
		'mujer': 'Mujer',
		'varon': 'Varón',
		'otro': 'Otro',

	}
	genero = models.CharField(max_length=20, choices=CHOICES_GENERO, verbose_name="Género")
	provincia = models.CharField(max_length=30, verbose_name="Lugar de residencia: [Provincia]")
	ciudad = models.CharField(max_length=30, verbose_name="Lugar de residencia: [Ciudad]")
	obra_social = models.CharField(max_length=30, blank=True, null=True, verbose_name="¿Cuenta con obra social (por ejemplo: APROSS, OSECAC, UOM, OSPACA, OSPECOM, UOCRA, UPCN, etc.)? ¿Cuál?")
	prepaga = models.CharField(max_length=30, blank=True, null=True, verbose_name="¿Cuenta con medicina prepaga o plan privado de salud (por ejemplo: GEA, MEDIFE, SIPSSA, OMINT, SWISS MEDICAL, etc.)? ¿Cuál?")
	servicio_publico = models.CharField(max_length=30, blank=True, null=True, verbose_name="¿Hace uso del sistema de servicios o programas públicos de salud (por ejemplo: Hospitales públicos, Dispensarios, Incluir Salud, etc.)? ¿Cuál?")
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

class Cpqol(models.Model):
	creacion = models.DateTimeField('creacion',auto_now_add=True)    
	user=models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
	codigo=models.CharField(max_length=30, blank=True, null=True)
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

	class Meta:
		verbose_name_plural = "Lista De Formularios"

	@property
	def current_seccion(self):
		if self.servicios: return 12
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
		return 0
	
	@property
	def confirmado(self):
		return self.servicios != None

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