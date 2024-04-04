from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


from .forms import *

# Create your views here.
@login_required
def formulario(request):

    numero_seccion = int(request.GET['seccion'])

    seccion = {
        1 : {'form': TutorForm, 'nombre': "Tutor"},
        2 : {'form': PacienteForm, 'nombre': "Paciente"},
        3 : {'form': SentimientosForm, 'nombre': "Sentimientos"},
        4 : {'form': RelacionesForm, 'nombre': "Relaciones"},
        5 : {'form': FamiliaForm, 'nombre': "Familia"},
        6 : {'form': ParticipacionForm, 'nombre': "Participacion"},
        7 : {'form': EscuelaForm, 'nombre': "Escuela"},
        8 : {'form': SaludForm, 'nombre': "Salud"},
        9 : {'form': DolorForm, 'nombre': "Dolor"},
        10 : {'form': ServiciosForm, 'nombre': "Servicios"},
    }[numero_seccion]

    seccion['numero'] = numero_seccion
    if numero_seccion > 1:
        seccion['anterior'] = numero_seccion -1

    current_form = seccion['form']


    if request.method == 'POST':
        form = current_form(request.POST)
        if numero_seccion <= 11:
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion+1}')
        else:
            return HttpResponseRedirect("home")
        # if form.is_valid():
        #     form.save()
            # hacer algo con el formulario válido
    else:
        form = current_form()

    contexto = {
        'form': form,
        'seccion': seccion
    }

    return render(request, "core/formulario.html", contexto)