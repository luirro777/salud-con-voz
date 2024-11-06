from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .resources import CpqolResource

from .forms import *

# Create your views here.
@login_required
def vista_formulario(request):

    # Obtenemos el grupo
    grupo = request.user.groups.first().name if request.user.groups.all() else "profesional"

    # Obtenemos numero de seccion
    numero_seccion = int(request.GET['seccion'])
    # Obtenemos cpqol si existe
    try:
        cpqol = Cpqol.objects.get(user=request.user, codigo=request.GET['codigo'])
    except:
        cpqol = None

    # Formularios
    secciones = [
        {'form': TerminosYCondicionesForm, 'nombre': "Términos y condiciones", 'subtitulo': ""},
        {'form': CodigoForm, 'nombre': "Código de participante", 'subtitulo': "Generación de código de identificación"},
        {'form': TutorForm, 'attr': "tutor", 'nombre': "Padre, madre o cuidador", 'subtitulo': 'Información general sobre la persona que responde'},
        {'form': PacienteForm, 'attr': "paciente", 'nombre': "Paciente", 'subtitulo': 'Datos generales de niño/a o adolescente'},
        {'form': SentimientosForm, 'attr': "sentimientos", 'nombre': "Sus sentimientos",  'subtitulo': ""},
        {'form': RelacionesForm, 'attr': "relaciones", 'nombre': "Relaciones con los demás", 'subtitulo': ''},
        {'form': FamiliaForm, 'attr': "familia", 'nombre': "Familia", 'subtitulo': ''},
        {'form': ParticipacionForm, 'attr': "participacion", 'nombre': "Participacion", 'subtitulo': ''},
        {'form': EscuelaForm, 'attr': "escuela", 'nombre': "Escuela o Colegio", 'subtitulo': ''},
        {'form': SaludForm, 'attr': "salud", 'nombre': "Salud", 'subtitulo': ''},
        {'form': DolorForm, 'attr': "dolor", 'nombre': "Dolor y molestias", 'subtitulo': ''},
        {'form': ServiciosForm, 'attr': "servicios", 'nombre': "Acceso a servicios", 'subtitulo': ''},
        {'form': None, 'nombre': "Informe de resultados", 'subtitulo': 'Calidad de vida relacionada con la salud en niñas, niños, adolescentes y jóvenes con parálisis cerebral'},
        {'form': Salud_ultimasemana_Form, 'nombre': "Más preguntas sobre la salud del niño/a o adolescente", 'subtitulo': 'Las siguientes preguntas son similares a algunas que ya respondió; pero ahora, por favor, piense en la última semana.'},
        {'form': Salud_ultimasemana2_Form, 'nombre': "Sobre la salud del chico o chica", 'subtitulo': 'Las preguntas a continuación corresponden a un cuestionario de salud que se aplica a cualquier niño/a o adolescente en cualquier situación (con o sin problemas de salud), por lo que pueden resultar difíciles de responder. Por favor, responda según lo mejor que usted conozca, asegurándose de que sus respuestas reflejen la perspectiva de su hijo/a. Trate de recordar las experiencias del chico/a durante la última semana.'},
        {'form': Caracteristicas_hogar_Form, 'nombre': "Características del hogar", 'subtitulo': 'Esta es la última parte de la encuesta y le solicitamos que responda acerca de algunas características del hogar donde vive la chica o el chico. Estos datos son muy importantes para analizar a qué hogares hemos podido llegar con este estudio, para ofrecer información sobre la población argentina con parálisis cerebral (recuerde que estos datos nunca se analizan ni informan individualmente).'},
        {'form': None, 'nombre': "Acceso a servicios", 'subtitulo': '"Agradecemos que se haya tomado el tiempo de completar estos cuestionarios que nos ayudan a conocer la calidad de vida de las infancias y juventudes con parálisis cerebral; si quisiera que nos comuniquemos con Ud. para continuar colaborando y conocer más sobre nuestro trabajo, por favor, escriba su dirección de correo electrónico".'},
    ]
    total_secciones = len(secciones) - 1
    
    seccion = secciones[numero_seccion]


    seccion['numero'] = numero_seccion
    seccion['siguiente'] = numero_seccion +1
    if numero_seccion > 1:
        seccion['anterior'] = numero_seccion -1

    current_form = seccion['form']


    if request.method == 'POST':
        form = current_form(request.user, request.POST)
        if form.is_valid():
            if numero_seccion == 0:
                return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion+1}')   
            elif numero_seccion == 1:
                cpqol = form.save()
            else:
                instance = form.save(cpqol, seccion['attr'].lower())
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion+1}&codigo={cpqol.codigo}')   
    else:
        if not numero_seccion == total_secciones:
            if numero_seccion > 1:
                instance = getattr(cpqol, seccion['attr'].lower(), None)
                form = current_form(instance=instance)
            else:
                form = current_form(request.user)

    if numero_seccion == 12: 
        labels = list(cpqol.resultados.keys())
        values = list(cpqol.resultados.values())

    return render(request, "core/formulario.html", locals())



def exportar_excel(request):
    modelo_resource = CpqolResource()
    dataset = modelo_resource.export(Cpqol.objects.filter(user=request.user))
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="resultados.xlsx"'
    return response