from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import *

# Create your views here.
@login_required
def vista_formulario(request):

    # Obtenemos numero de seccion
    numero_seccion = int(request.GET['seccion'])
    # Obtenemos cpqol si existe
    try:
        cpqol = Cpqol.objects.get(user=request.user, codigo=request.GET['codigo'])
    except:
        cpqol = None

    # Formularios
    seccion = [
        {'form': CodigoForm, 'nombre': "Código"},
        {'form': TutorForm, 'nombre': "Tutor", 'subtitulo': 'Información general sobre la persona que responde'},
        {'form': PacienteForm, 'nombre': "Paciente", 'subtitulo': 'Datos generales de niño/a o adolescente'},
        {'form': SentimientosForm, 'nombre': "Sentimientos",  'subtitulo': "¿Cómo piensa que su hijo/a se siente con respecto a..."},
        {'form': RelacionesForm, 'nombre': "Relaciones", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': FamiliaForm, 'nombre': "Familia", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': ParticipacionForm, 'nombre': "Participacion", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': EscuelaForm, 'nombre': "Escuela", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': SaludForm, 'nombre': "Salud", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': DolorForm, 'nombre': "Dolor", 'subtitulo': '¿Cómo piensa que su hijo/a se siente con respecto a...'},
        {'form': ServiciosForm, 'nombre': "Servicios", 'subtitulo': '¿Cómo se siente USTED con respecto a...'},
    ][numero_seccion]

    seccion['numero'] = numero_seccion
    if numero_seccion > 1:
        seccion['anterior'] = numero_seccion -1

    current_form = seccion['form']


    if request.method == 'POST':
        form = current_form(request.POST)
        if form.is_valid():
            if numero_seccion == 0:
                cpqol = form.save(request.user)
            else:
                instance = form.save(cpqol, seccion['nombre'].lower())
        if numero_seccion <= 11:
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion+1}&codigo={cpqol.codigo}')
        else:
            return HttpResponseRedirect("home")
    else:
        if numero_seccion >= 1:
            instance = getattr(cpqol, seccion['nombre'].lower(), None)
            form = current_form(instance=instance)
        else:
            form = current_form()

    # contexto = {
    #     'form': form,
    #     'seccion': seccion
    # }

    return render(request, "core/formulario.html", locals())