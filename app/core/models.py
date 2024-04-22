from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

class Paciente(models.Model):
	edad = models.IntegerField(blank=True, null=True, verbose_name="Edad: [De la persona que responde]")
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

CHOICES_SENTIMIENTOS = {
	1:'1 - Muy Desconforme',
	2:'2 - Muy Desconforme',
	3:'3 - Desconforme',
	4:'4 - Desconforme',
	5:'5 - Ni conforme ni desconforme',
	6:'6 - Ni conforme ni desconforme',
	7:'7 - Conforme',
	8:'8 - Conforme',
	9:'9 - Muy Conforme',
	}

CHOICES_DOLOR = {
	1:'1 - Nada de dolor',
	2:'2 - Nada de dolor',
	3:'3 - Nada de dolor',
	4:'4 - Nada de dolor',
	5:'5 - Nada de dolor',
	6:'6 - Mucho dolor',
	7:'7 - Mucho dolor',
	8:'8 - Mucho dolor',
	9:'9 - Mucho dolor',
	}

CHOICES_MOLESTIA = {
	1:'1 - Nada molesto',
	2:'2 - Nada molestor',
	3:'3 - Nada molestor',
	4:'4 - Nada molesto',
	5:'5 - Muy molesto',
	6:'6 - Muy molesto',
	7:'7 - Muy molesto',
	8:'8 - Muy molesto',
	9:'9 - Muy molesto',
	}

class Sentimientos(models.Model):
	hacer_cosas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	uno_mismo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	motivacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	oportunidades = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	aspecto_fisico = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Relaciones(models.Model):
	con_gente = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	otros_chichos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	con_adultos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	con_amigos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	aceptacion_otros_chicos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	aceptacion_adultos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	aceptacion_gente = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	cosas_nuevas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	comunicacion_conocidos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	comunicacion_extranios = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	comunicacion_otros_con_el = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	comunicacion_tecnologia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Familia(models.Model):
	apoyo_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	viaje_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	aceptacion_flia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Participacion(models.Model):
	recreativas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	deportivas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	eventos_sociales = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)  
	en_su_comunidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Escuela(models.Model):
	otros_chicos_escuela = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	como_lo_integran= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	profesores = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)  
	otros_alumnos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	otros_docentes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	mismo_trato = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	participacion_colegio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Salud(models.Model):
	hacer_cosas_solo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	movilidad= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	independencia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)  
	moverse_dentro_barrio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	transporte = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	brazos_y_manos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	piernas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	vestirse = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	beber = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	ir_al_banio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)

class Dolor(models.Model):
	salud_gral = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	suenio= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	cuanto_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_DOLOR)  
	nivel_dolor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA)
	nivel_incomodidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA)
	como_afecta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA)
	impedimentos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA)
	no_disfrutar_dia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_MOLESTIA)

class Servicios(models.Model):
	acceso_tratamiento = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS)
	acceso_terapia= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	acceso_terapia= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	acceso_atencion_medica= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	acceso_pediatria= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 
	acceso_ayuda_aprendizaje= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], choices=CHOICES_SENTIMIENTOS) 

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

	@property
	def current_seccion(self):
		if not self.tutor: return 1 
		if not self.paciente: return 2
		if not self.sentimientos: return 3
		if not self.relaciones: return 4
		if not self.familia: return 5
		if not self.participacion: return 6
		if not self.escuela: return 7
		if not self.salud: return 8
		if not self.dolor: return 9 
		if not self.servicios: return 10
		return 0