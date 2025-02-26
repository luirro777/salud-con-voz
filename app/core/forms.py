from typing import Any
from django import forms

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
    nombre = forms.CharField(label="Ingrese la inicial del primer nombre", min_length=1, max_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label="Ingrese la inicial del primer apellido", min_length=1, max_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        mes_ano = cleaned_data.get('mes_ano')
        dni = cleaned_data.get('dni')
        nombre = cleaned_data.get('nombre').upper()
        apellido = cleaned_data.get('apellido').upper()
        codigo = f'{self.user.username}-{mes_ano}{dni}{nombre}{apellido}'
        try:
            _ = Cpqol.objects.get(
                user=self.user,
                codigo=codigo
            )
            self.add_error('dni', "Ya posee un CPQOL con esta combinación")
        except:
            pass
            
        return cleaned_data
    


    def save(self):
        dni = self.cleaned_data.get('dni')
        mes_ano = self.cleaned_data.get('mes_ano')
        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre').upper()
        apellido = self.cleaned_data.get('apellido').upper()
        codigo = f'{self.user.username}-{mes_ano}{dni}{nombre}{apellido}'
        cpqol_instance = Cpqol.objects.create(
            user=self.user,
            codigo=codigo
        )
        return cpqol_instance

    def help_text(self):
        return """
Esta plataforma es segura y sus
responsables se comprometen a respetar la confidencialidad de la información que
ingrese. Igualmente, por razones éticas y de seguridad, ahora se generará un código
anónimo único por participante para que no se pueda identificar a las personas con las
respuestas, pero que en el futuro facilite reunir datos de la misma persona bajo ese
código.
"""

class BaseForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user        
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control h5'})


    def save(self, cpqol, atributo):
        instance = super().save(commit=True)
        setattr(cpqol, atributo, instance)
        cpqol.save()
        return instance


class TutorForm(BaseForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        widgets = {
            'estado_salud': forms.RadioSelect,
        }
'''
class PacienteForm(BaseForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            "fecha_nacimiento": forms.DateInput,
        }
'''


class PacienteForm(BaseForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                format='%d/%m/%Y',  
                attrs={
                    'type': 'date',  
                    #'class': 'form-control',  
                }
            ),
        }
'''
class MovimientoForm(BaseForm):
    class Meta:
        model = Movimiento
        fields = '__all__'

'''


class MovimientoForm(BaseForm):
    class Meta:
        model = Movimiento
        fields = '__all__'
        widgets = {
            'movimiento': forms.Select,  
        }

    def __init__(self, edad=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_name = "MovimientoForm"        
        
        if edad is not None:
            edad = int(str(edad))
            if 4 <= edad <= 6:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones."),
                    (2, "Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda y supervisión de un adulto."),
                    (3, "Puede caminar usando alguna ayuda para la marcha (como un andador, bastones o muletas)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero con dificultad para largas distancias o terreno irregular."),
                    (5, "Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares."),
                ]

                help_text = """               
                
                **Ayuda para responder:**
                1. Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones.
                Dificultad para el control voluntario de cualquier movimiento. Para una sedestación confortable necesita adaptaciones
                especiales en la silla. Para trasladarlo tiene que ser cogido en brazos por otra persona.

                2. Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda y supervisión de un adulto.
                Puede necesitar soporte del tronco para mejorar la función del brazo y de la mano. Normalmente necesita la ayuda de un adulto para
                sentarse o levantarse de una silla. Con silla de ruedas eléctrica puede desplazarse de manera independiente en exteriores o en 
                silla manual propulsada por otra persona.

                3. Puede caminar usando alguna ayuda para la marcha (como un andador, bastones o muletas).
                Es capaz de sentarse y levantarse de una silla sin ayuda. Puede necesitar de una silla de ruedas para largas distancias o fuera
                de casa. Tiene difucultad para subir escaleras o caminar por terreno irregular sin una ayuda considerable.

                4. Puede caminar sin ayudas para la marcha, pero con dificultad para largas distancias o terreno irregular.
                Es capaz de sentarse en una silla normal de adulto, sin ayuda de las manos. Puede ponerse de pie desde el suelo, sin ayuda 
                de un adulto. Necesita apoyarse en el pasamanos para subir y bajar escaleras. Todavía no es capaz de correr ni de saltar.

                5. Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares.
                Puede ponerse de pie desde el suelo o levantarse de una silla sin usar las manos como apoyo. Es capaz de subir y bajar 
                escaleras sin apoyarse en el pasamanos. Comienza a correr y saltar.
                """
            elif 7 <= edad <= 11:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones."),
                    (2, "Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda."),
                    (3, "Es capaz de mantenerse de pie por sí mismo y de caminar sólo si usa alguna ayuda para la marcha (andador, muletas, bastones)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras."),
                    (5, "Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares."),
                ]
                help_text = """
                                
                **Ayuda para responder:**
                1. Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en la mayoría de las posiciones.
                Tiene dificultad para controlar cualquier movimiento voluntario. Para una sedestación confortable necesita una silla 
                especialmente adaptada. Para trasladarlo tiene que ser cogido en brazos por otra persona.

                2. Puede mantenerse sentado, pero no es capaz de mantenerse de pie o caminar sin gran ayuda.
                Está la mayor parte del tiempo en silla de ruedas en casa, en la escuela y en la comunidad. A menudo necesita soportes de 
                tronco para mejorar la función del brazo y de la mano. Puede desplazarse de manera independiente con una silla de ruedas 
                eléctrica.

                3. Es capaz de mantenerse de pie por sí mismo y de caminar sólo si usa alguna ayuda para la marcha (andador, muletas, bastones).
                Le resulta difícil subir escaleras o caminar sobre una superficie irregular. Puede necesitar una silla para desplazamientos 
                largos o en espacios multitudinarios.

                4. Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras.
                Habitualmente tiene dificultad para caminar por superficies irregulares o pendientes o en espacios multitudinarios.

                5. Puede caminar sin ayudas para la marcha, incluyendo largas distancias en exteriores y superficies irregulares.
                Puede ponerse de pie desde el suelo o levantarse de una silla sin usar las manos como apoyo. Es capaz de subir y bajar 
                escaleras sin apoyarse en el pasamanos. Comienza a correr y saltar
                """
            elif edad >= 12:
                opciones = [
                    (1, "Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en cualquier posición."),
                    (2, "Puede mantenerse sentado con algún soporte en pelvis o en tronco, pero no estar de pie, ni caminar sin gran apoyo."),
                    (3, "Es capaz de mantenerse de pie por sí mismo y de caminar, sólo si usa alguna ayuda para la marcha (como un andador, muletas, bastones, etc.)."),
                    (4, "Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras."),
                    (5, "Puede caminar sin ayudas para la marcha y subir y bajar escaleras sin necesidad de apoyarse en el pasamanos."),
                ]
                help_text = """
                                
                **Ayuda para responder:**
                1. Tiene dificultad para mantenerse sentado y para controlar la cabeza y el tronco en cualquier posición.
                Tiene dificultad para controlar cualquier movimiento voluntario. Necesita una silla con adaptaciones especiales 
                para estar confortablemente sentado y para sus desplazamientos. Para trasladarlo, tiene que ser cogido en brazos por otra 
                persona o usar grúa.

                2. Puede mantenerse sentado con algún soporte en pelvis o en tronco, pero no estar de pie, ni caminar sin gran apoyo.
                Siempre usa silla de ruedas en el exterior. Puede desplazarse de manera autónoma en una silla de ruedas eléctrica.
                Dentro de casa, puede arrastrarse o voltearse distancias pequeñas.

                3. Es capaz de mantenerse de pie por sí mismo y de caminar, sólo si usa alguna ayuda para la marcha (como un andador, muletas, bastones, etc.).
                Le resulta difícil subir escaleras o caminar sobre una superficie irregular sin ayuda. Para desplazarse utiliza muchos métodos, 
                dependiendo de las circunstancias. Prefiere usar una silla de ruedas para desplazarse rápidamente o para largas distancias.

                4. Puede caminar sin ayudas para la marcha, pero necesita apoyarse en el pasamanos para subir y bajar escaleras.
                Habitualmente camina en la mayoría de los entornos.Normalmente tiene dificultades para caminar por terreno irregular, 
                pendientes o en espacios multitudinarios. De vez en cuando prefiere utilizar ayudas para la marcha (bastones o muletas) o 
                una silla de ruedas para desplazarse rápidamente o para largas distancias.

                5. Puede caminar sin ayudas para la marcha y subir y bajar escaleras sin necesidad de apoyarse en el pasamanos.
                Camina por cualquier parte (incluyendo terreno irregular, pendientes o espacios multitudinarios). Puede correr y saltar, 
                aunque su velocidad, equilibrio y coordinación estén ligeramente limitadas.
                """
            else:
                opciones = []
                help_text = "Por favor, seleccione la opción que mejor describa la capacidad de su hijo/a para moverse."

            self.fields['movimiento'].choices = opciones
            self.fields['movimiento'].help_text = help_text

'''
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

'''

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
        self.help_text = """
        Queremos preguntarle sobre cómo piensa que su hijo/a SE SIENTE respecto a algunos aspectos de su vida, como su familia,
        amigos, salud y escuela. El cuestionario mide cómo se siente su hijo/a, no lo que puede hacer.
        Cuando lea las preguntas, piense que no hay respuestas correctas e incorrectas, sino que es importante que responda lo 
        que es más adecuado a su caso. En cada pregunta, marque con un círculo el número que mejor exprese cómo piensa usted que 
        SE SIENTE su hijo/a. Puede escoger cualquier número del 1 (Muy desconforme) al 9 (Muy conforme).
        """



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
'''
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
'''

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
        self.fields['brazos_y_manos'].help_text = """
        Las próximas 2 preguntas se refieren a cómo se siente su hijo/a con respecto al uso de partes de su cuerpo, no si su hijo/a 
        puede usar parte de su cuerpo.
        """
        
        # Texto antes de "vestirse"
        self.fields['vestirse'].help_text = """
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
        self.fields['cuanto_dolor'].help_text = """
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
                    "caminar": forms.RadioSelect,
                    "caminar_2": forms.RadioSelect,
                    "bañarse": forms.RadioSelect,
                    "bañarse_2": forms.RadioSelect,
                    "ir_baño": forms.RadioSelect,
                    "ir_baño_2": forms.RadioSelect,
                    "comunicarse": forms.RadioSelect,
                    "comunicarse_2": forms.RadioSelect,
                    "hablar": forms.RadioSelect,
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







