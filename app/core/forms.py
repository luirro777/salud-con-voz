from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .help_texts import (
    MOVIMIENTO_HELP_TEXT_4_6,
    MOVIMIENTO_HELP_TEXT_7_11,
    MOVIMIENTO_HELP_TEXT_12,
    CODIGO_HELP_TEXT,
    SENTIMIENTOS_HELP_TEXT,
)
from .models import *

class TerminosYCondicionesForm(forms.Form):

    consentimiento = forms.BooleanField(label="He leído esta información sobre la investigación y acepto participar.")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user    
        super().__init__(*args, **kwargs)

    def save(self):
        return        
    

class CodigoForm(forms.Form):
    mes_ano = forms.CharField(label="Ingrese Mes y Año de Nacimiento (del paciente) en formato MMAA", min_length=4, max_length=4, widget=forms.TextInput(attrs={'class': 'form-control',}))
    dni = forms.CharField(label="Ingrese los últimos 3 números del DNI del paciente", min_length=3, max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Ingrese la inicial del primer nombre del paciente", min_length=1, max_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label="Ingrese la inicial del primer apellido del paciente", min_length=1, max_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def __init__(self, user=None, grupo=None, *args, **kwargs):
        self.user = user
        self.grupo = grupo
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        mes_ano = cleaned_data.get('mes_ano')
        dni = cleaned_data.get('dni')
        nombre = cleaned_data.get('nombre').upper()
        apellido = cleaned_data.get('apellido').upper() 
        
        sufijo = ''
        if self.grupo == "profesional":
            sufijo = 'P'
            ModelToUse = CpqolProfesional
        else: 
            sufijo = 'F'
            ModelToUse = Cpqol
            
        codigo = f'{mes_ano}{dni}{nombre}{apellido}{sufijo}'
        cleaned_data["sufijo"] = sufijo 
        cleaned_data['codigo'] = codigo     

        try:
            _ = ModelToUse.objects.get(
                user=self.user,
                codigo=codigo
            )
            self.add_error('dni', "Ya posee un CPQOL con esta combinación")
        except ModelToUse.DoesNotExist:
            pass
            
        return cleaned_data
    


    def save(self):
        dni = self.cleaned_data.get('dni')
        mes_ano = self.cleaned_data.get('mes_ano')
        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre').upper()
        apellido = self.cleaned_data.get('apellido').upper()
        sufijo = self.cleaned_data.get('sufijo')
        codigo = f'{mes_ano}{dni}{nombre}{apellido}{sufijo}'

        if self.grupo == "profesional":
            cpqol_instance = CpqolProfesional.objects.create(
                user=self.user,
                codigo=codigo
            )
        else:
            cpqol_instance = Cpqol.objects.create(
                user=self.user,
                codigo=codigo
            )
        return cpqol_instance

    def help_text(self):
        return CODIGO_HELP_TEXT

class BaseForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user        
        super().__init__(*args, **kwargs)
        if 'promedio' in self.fields:
            del self.fields['promedio']
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control h5'})


    def save(self, cpqol, atributo):
        instance = super().save(commit=True)
        setattr(cpqol, atributo, instance)
        cpqol.save()
        return instance
########################################################    
# Para encuesta de profesionales
# En tu forms.py
class ProfesionalForm(BaseForm):
    class Meta:
        model = Profesional
        fields = [
            'profesion', 
            'especialidad', 
            'profesion_otra', 
            'provincia_atencion', 
            'ciudad_atencion', 
            'tipo_centro',
            'tipo_centro_otro', 
            'centro_salud'
        ]
        widgets = {
            'profesion': forms.Select(attrs={'class': 'form-control h5'}),
            'especialidad': forms.TextInput(attrs={'placeholder': 'Especialidad', 'class': 'form-control h5'}),
            'profesion_otra': forms.TextInput(attrs={'placeholder': 'Especifique la profesión', 'class': 'form-control h5'}),
            'provincia_atencion': forms.TextInput(attrs={'placeholder': 'Provincia donde atiende', 'class': 'form-control h5'}),
            'ciudad_atencion': forms.TextInput(attrs={'placeholder': 'Ciudad o localidad', 'class': 'form-control h5'}),
            'tipo_centro': forms.Select(attrs={'class': 'form-control h5'}),
            'centro_salud': forms.TextInput(attrs={'placeholder': 'Nombre del centro o servicio', 'class': 'form-control h5'}),
        }

    


class ContextoForm(BaseForm):
    class Meta:
        model = Contexto
        fields = ['persona_ocupa', 'max_estudios', 'edad', 'genero']
        widgets = {
            'persona_ocupa': forms.Select(attrs={'class': 'form-control h5'}),
            'max_estudios': forms.Select(attrs={'class': 'form-control h5'}),
            'edad': forms.NumberInput(attrs={'min': 0, 'max': 18, 'class': 'form-control h5'}),
            'genero': forms.Select(attrs={'class': 'form-control h5'}),
        }

    


class DatosClinicosForm(BaseForm):
    class Meta:
        model = DatosClinicos
        fields = ['gmfcs', 'macs', 'cfcs', 'edacs']
        widgets = {
            'gmfcs': forms.Select(attrs={'class': 'form-control h5'}),
            'macs': forms.Select(attrs={'class': 'form-control h5'}),
            'cfcs': forms.Select(attrs={'class': 'form-control h5'}),
            'edacs': forms.Select(attrs={'class': 'form-control h5'}),
        }

    

# Este paso es tanto para profesionales, como para familiares
class FinalizacionForm(BaseForm):
    # campo extra para la confirmación del correo.    
    correo_confirmacion = forms.EmailField(
        max_length=254,
        required=False,
        initial='correo@ejemplo.com',
        widget=forms.EmailInput(attrs={'placeholder': 'Confirme su correo', 'class': 'form-control h5'}),
        label="Confirme su correo electrónico"
    )

    class Meta:
        model = Finalizacion
        fields = ['correo']
        widgets = {
            'correo': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com', 'class': 'form-control h5'}),
        }

    # Validación
    def clean(self):        
        cleaned_data = super().clean()        
        correo = cleaned_data.get('correo')
        correo_confirmacion = cleaned_data.get('correo_confirmacion')        
        if correo and correo_confirmacion and correo != correo_confirmacion:
            raise ValidationError("Los correos electrónicos no coinciden.")
        
        return cleaned_data


################################################
# Para encuesta de cuidadores
class TutorForm(BaseForm):
    class Meta:
        model = Tutor
        fields = '__all__'        
        widgets = {
            'estado_salud': forms.RadioSelect,
        }
    def clean(self):
        cleaned_data = super().clean()
        quien_cuida = cleaned_data.get("quien_cuida")
        quien_cuida_otro = cleaned_data.get("quien_cuida_otro")
        if quien_cuida in ['con-ayuda', 'otra-persona', 'otra-opcion'] and not quien_cuida_otro:
            self.add_error("quien_cuida_otro", f"Este campo es obligatorio para la opción seleccionada.")
        relacion = cleaned_data.get("relacion")
        relacion_otro = cleaned_data.get("relacion_otro")
        if relacion in ['otro-familiar', 'otra-persona-no-familiar'] and not relacion_otro:
            self.add_error("relacion_otro", "Este campo es obligatorio para la opción seleccionada.")
        genero = cleaned_data.get("genero")
        genero_otro = cleaned_data.get("genero_otro")
        if genero == 'otro' and not genero_otro:
            self.add_error("genero_otro", "Este campo es obligatorio para la opción seleccionada.")
        return cleaned_data



class PacienteForm(BaseForm):
    cobertura = forms.MultipleChoiceField(
        choices=Paciente.CHOICES_COBERTURA.items(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="¿Qué tipo de cobertura de salud tiene su hijo/a actualmente?"
    )
    
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                format='%d/%m/%Y',  
                attrs={
                    'type': 'date',  
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        cobertura = cleaned_data.get("cobertura")
        cobertura_cual = cleaned_data.get("cobertura_cual")        
        if cobertura and any(opcion in cobertura for opcion in ["obra_social", "prepaga_obra_social", "prepaga_voluntaria"]):
            if not cobertura_cual:
                self.add_error("cobertura_cual", "Este campo es obligatorio para la opción seleccionada.")
        return cleaned_data

    def save(self, commit=True):
        # Guardar el campo cobertura como JSON
        instance = super().save(commit=False)
        if 'cobertura' in self.cleaned_data:
            instance.cobertura = self.cleaned_data['cobertura']
        if commit:
            instance.save()
        return instance


class MovimientoForm(BaseForm):
    class Meta:
        model = Movimiento
        fields = '__all__'
        widgets = {
            'movimiento': forms.Select,
        }

    def __init__(self, *args, edad=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_name = "MovimientoForm"

        if edad is not None:
            try:
                edad = int(edad)
            except (ValueError, TypeError):
                raise ValueError(f"El valor de edad es inválido: {edad}")            
           
            opciones = []
            help_text = ""

            if 0 <= edad <= 6:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones."),
                    (2, "Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda y supervisión de un adulto."),
                    (3, "Puede caminar usando alguna ayuda para la marcha (como un andador, bastones o muletas)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero con dificultad para largas distancias o terreno irregular."),
                    (5, "Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares."),
                ]
                help_text = MOVIMIENTO_HELP_TEXT_4_6
            elif 7 <= edad <= 11:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones."),
                    (2, "Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda."),
                    (3, "Es capaz de mantenerse de pie por sí mismo y de caminar sólo si usa alguna ayuda para la marcha (andador, muletas, bastones)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras."),
                    (5, "Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares."),
                ]
                help_text = MOVIMIENTO_HELP_TEXT_7_11
            elif edad >= 12:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en cualquier posición."),
                    (2, "Puede mantenerse sentado con algún soporte en pelvis o en tronco, pero no estar de pie, ni caminar sin gran apoyo."),
                    (3, "Es capaz de mantenerse de pie por sí mismo y de caminar, sólo si usa alguna ayuda para la marcha (como un andador, muletas, bastones, etc.)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras."),
                    (5, "Puede caminar sin ayudas para la marcha y subir y bajar escaleras sin necesidad de apoyarse en el pasamanos."),
                ]
                help_text = MOVIMIENTO_HELP_TEXT_12
            else:
                opciones = []
                help_text = "Por favor, seleccione la opción que mejor describa la capacidad de su hijo/a para moverse."

            self.fields['movimiento'].choices = [('', '-------------')] + opciones
            self.fields['movimiento'].help_text = help_text
            self.fields['movimiento'].required = True  
        



class SentimientosForm(BaseForm):
    class Meta:
        model = Sentimientos
        fields = '__all__'
        widgets = {
            "hacer_cosas": forms.RadioSelect,
            "uno_mismo": forms.RadioSelect,
            "motivacion": forms.RadioSelect,
            "oportunidades": forms.RadioSelect,
            "aspecto_fisico": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar el help_text como un atributo del formulario
        self.help_text = SENTIMIENTOS_HELP_TEXT



class RelacionesForm(BaseForm):
    class Meta:
        model = Relaciones
        fields = '__all__'
        widgets = {
            "con_gente": forms.RadioSelect,
            "otros_chichos": forms.RadioSelect,
            "con_adultos": forms.RadioSelect,
            "con_amigos": forms.RadioSelect,
            "aceptacion_otros_chicos": forms.RadioSelect,
            "aceptacion_adultos": forms.RadioSelect,
            "aceptacion_gente": forms.RadioSelect,
            "cosas_nuevas": forms.RadioSelect,
            "comunicacion_conocidos": forms.RadioSelect,
            "comunicacion_extranios": forms.RadioSelect,
            "comunicacion_otros_con_el": forms.RadioSelect,
            "comunicacion_tecnologia": forms.RadioSelect,
        }        

class FamiliaForm(BaseForm):
    class Meta:
        model = Familia
        fields = '__all__'
        widgets = {
            "apoyo_flia": forms.RadioSelect,
            "viaje_flia": forms.RadioSelect,
            "aceptacion_flia": forms.RadioSelect,
        }                

class ParticipacionForm(BaseForm):
    class Meta:
        model = Participacion
        fields = '__all__'
        widgets = {
            "recreativas": forms.RadioSelect,
            "deportivas": forms.RadioSelect,
            "eventos_sociales": forms.RadioSelect,
            "en_su_comunidad": forms.RadioSelect,
        }                        

class EscuelaForm(BaseForm):
    class Meta:
        model = Escuela
        fields = '__all__'
        widgets = {
            "otros_chicos_escuela": forms.RadioSelect,
            "como_lo_integran": forms.RadioSelect,
            "profesores": forms.RadioSelect,
            "otros_alumnos": forms.RadioSelect,
            "otros_docentes": forms.RadioSelect,
            "mismo_trato": forms.RadioSelect,
            "participacion_colegio": forms.RadioSelect,
        }                


class SaludForm(BaseForm):
    class Meta:
        model = Salud
        fields = '__all__'
        widgets = {
            "hacer_cosas_solo": forms.RadioSelect,
            "movilidad": forms.RadioSelect,
            "independencia": forms.RadioSelect,
            "moverse_dentro_barrio": forms.RadioSelect,
            "transporte": forms.RadioSelect,
            "brazos_y_manos": forms.RadioSelect,
            "piernas": forms.RadioSelect,
            "vestirse": forms.RadioSelect,
            "beber": forms.RadioSelect,
            "ir_al_banio": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Texto antes de "brazos_y_manos"
        self.fields['transporte'].help_text = """
        Las próximas 2 preguntas se refieren a cómo se siente su hijo/a con respecto al uso de partes de su cuerpo, no si su hijo/a 
        puede usar parte de su cuerpo.
        """
        
        # Texto antes de "vestirse"
        self.fields['piernas'].help_text = """
        Las próximas 3 preguntas se refieren a cómo se siente su hijo/a con respecto a su capacidad de realizar actividades diarias, 
        no si su hijo/a puede realizarlas.
        """

class DolorForm(BaseForm):
    class Meta:
        model = Dolor
        fields = '__all__'
        widgets = {
            "salud_gral": forms.RadioSelect,
            "suenio": forms.RadioSelect,
            "cuanto_dolor": forms.RadioSelect,
            "nivel_dolor": forms.RadioSelect,
            "nivel_incomodidad": forms.RadioSelect,
            "como_afecta": forms.RadioSelect,
            "impedimentos": forms.RadioSelect,
            "no_disfrutar_dia": forms.RadioSelect,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar el help_text al campo "cuanto_dolor"
        self.fields['suenio'].help_text = """
        La siguiente pregunta se refiere al dolor que pueda sentir su hijo/a:
        """             

class ServiciosForm(BaseForm):
    class Meta:
        model = Servicios
        fields = '__all__'
        widgets = {
            "acceso_tratamiento": forms.RadioSelect,
            "acceso_terapia": forms.RadioSelect,
            "acceso_atencion_medica": forms.RadioSelect,
            "acceso_pediatria": forms.RadioSelect,
            "acceso_ayuda_aprendizaje": forms.RadioSelect,
        }                    

class SaludUltimaSemanaForm(BaseForm):
    class Meta:
        model = SaludUltimaSemana
        fields = '__all__'
        widgets = {
                    "frustra": forms.RadioSelect,
                    "correr": forms.RadioSelect,
                    "nadar": forms.RadioSelect,
                    "vestirse": forms.RadioSelect,
                    "inteligencia": forms.RadioSelect,
                    "edificios": forms.RadioSelect,
                    "piernas": forms.RadioSelect,
                    #"caminar": forms.RadioSelect,
                    "caminar_2": forms.RadioSelect,
                    #"bañarse": forms.RadioSelect,
                    "bañarse_2": forms.RadioSelect,
                    #"ir_baño": forms.RadioSelect,
                    "ir_baño_2": forms.RadioSelect,
                    #"comunicarse": forms.RadioSelect,
                    "comunicarse_2": forms.RadioSelect,
                    #"hablar": forms.RadioSelect,
                    "hablar_2": forms.RadioSelect
        } 

class SaludUltimaSemana2Form(BaseForm):
    class Meta:
        model = SaludUltimaSemana2
        fields = '__all__'
        widgets = {
                    "fisicamente": forms.RadioSelect,
                    "energia": forms.RadioSelect,
                    "tristeza": forms.RadioSelect,
                    "soledad": forms.RadioSelect,
                    "tiempo_libre": forms.RadioSelect,
                    "cosas_queria": forms.RadioSelect,
                    "justicia": forms.RadioSelect,
                    "diversion": forms.RadioSelect,
                    "colegio": forms.RadioSelect,
                    "atencion": forms.RadioSelect
        }   

class HogarForm(BaseForm):
    class Meta:
        model = Hogar
        fields = '__all__'
        widgets = {
                    "dormitorio_propio": forms.RadioSelect,
                    "autos": forms.RadioSelect,
                    "computadoras": forms.RadioSelect,
                    "duchas": forms.RadioSelect,
                    "lavaplatos": forms.RadioSelect,
                    "tareas_hogar": forms.RadioSelect,
                    "vacaciones": forms.RadioSelect,
                    "nivel_estudio": forms.RadioSelect,
                    "sosten_economico": forms.RadioSelect,
                    "nivel_estudio_2": forms.RadioSelect
                    }







