from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        {'form': TutorForm, 'nombre': "Padre, madre o cuidador", 'subtitulo': 'Información general sobre la persona que responde'},
        {'form': PacienteForm, 'nombre': "Paciente", 'subtitulo': 'Datos generales de niño/a o adolescente'},
        {'form': SentimientosForm, 'nombre': "Sentimientos",  'subtitulo': "Datos sobre sus sentimientos"},
        {'form': RelacionesForm, 'nombre': "Relaciones", 'subtitulo': 'Datos sobre sus relaciones con los demás'},
        {'form': FamiliaForm, 'nombre': "Familia", 'subtitulo': 'Datos sobre su familia'},
        {'form': ParticipacionForm, 'nombre': "Participacion", 'subtitulo': 'Datos sobre su participación'},
        {'form': EscuelaForm, 'nombre': "Escuela", 'subtitulo': 'Datos sobre su escuela o colegio'},
        {'form': SaludForm, 'nombre': "Salud", 'subtitulo': 'Datos sobre su salud'},
        {'form': DolorForm, 'nombre': "Dolor", 'subtitulo': 'Datos sobre sus dolores y/o molestias'},
        {'form': ServiciosForm, 'nombre': "Servicios", 'subtitulo': 'Datos sobre accesos a servicios'},
        {'form': None, 'nombre': "Informe de resultados", 'subtitulo': 'Calidad de vida relacionada con la salud en niñas, niños, adolescentes y jóvenes con parálisis cerebral'},
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
                instance = form.save(cpqol, seccion['nombre'].lower())
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion+1}&codigo={cpqol.codigo}')   
    else:
        if not numero_seccion == total_secciones:
            if numero_seccion > 1:
                instance = getattr(cpqol, seccion['nombre'].lower(), None)
                form = current_form(instance=instance)
            else:
                form = current_form(request.user)

    return render(request, "core/formulario.html", locals())