from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from core.models import Cpqol

@login_required
def home(request):

    cuestionarios = Cpqol.objects.filter(user=request.user)

    contexto = {
        'cuestionarios': cuestionarios
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