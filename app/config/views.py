from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from itertools import chain
from core.models import Cpqol, CpqolProfesional

@login_required
def home(request):
    grupo = request.user.groups.first().name if request.user.groups.all() else "profesional" # Asumo que "profesional" es el default si no hay grupo explícito

    cuestionarios = None
    if grupo == "profesional":
        cuestionarios = CpqolProfesional.objects.filter(user=request.user)
    elif grupo == "familiar": 
        cuestionarios = Cpqol.objects.filter(user=request.user)
    elif grupo == "coordinacion":
        cuestionarios_prof = list(CpqolProfesional.objects.all())
        cuestionarios_fam = list(Cpqol.objects.all())        
        for c in cuestionarios_prof:
            c.tipo = 'profesional'
        for c in cuestionarios_fam:
            c.tipo = 'familiar'  
        cuestionarios = list(chain(cuestionarios_prof, cuestionarios_fam))
    contexto = {
        'cuestionarios': cuestionarios,
        'grupo': grupo,
    }

    return render(request, "home/index.html", contexto)

class SaludConVozView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        # Llamar al contexto predeterminado
        context = super().get_context_data(**kwargs)

        # Agregar datos dinámicos al contexto
        context['ciess_link'] = 'https://example.com/ciess'
        context['ciecs_link'] = 'https://example.com/ciecs'

        # Retornar el contexto
        return context