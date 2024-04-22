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
        {'form': CodigoForm, 'nombre': "Codigo"},
        {'form': TutorForm, 'nombre': "Tutor"},
        {'form': PacienteForm, 'nombre': "Paciente"},
        {'form': SentimientosForm, 'nombre': "Sentimientos"},
        {'form': RelacionesForm, 'nombre': "Relaciones"},
        {'form': FamiliaForm, 'nombre': "Familia"},
        {'form': ParticipacionForm, 'nombre': "Participacion"},
        {'form': EscuelaForm, 'nombre': "Escuela"},
        {'form': SaludForm, 'nombre': "Salud"},
        {'form': DolorForm, 'nombre': "Dolor"},
        {'form': ServiciosForm, 'nombre': "Servicios"},
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
        instance = getattr(cpqol, seccion['nombre'].lower(), None)
        form = current_form(instance=instance)

    # contexto = {
    #     'form': form,
    #     'seccion': seccion
    # }

    return render(request, "core/formulario.html", locals())