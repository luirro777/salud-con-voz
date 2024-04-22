from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Cpqol

@login_required
def home(request):

    cuestionarios = Cpqol.objects.filter(user=request.user)

    contexto = {
        'cuestionarios': cuestionarios
    }

    return render(request, "home/index.html", contexto)
