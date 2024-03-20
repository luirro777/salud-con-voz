from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    cuestionarios = [
        {'id': 1, 'codigo': 'akosdjasd-1516', 'fecha': "15/03/2024", 'tipo': "familiar", 'confirmado': "SI"},
        {'id': 2, 'codigo': 'akosdjasd-1517', 'fecha': "15/03/2024", 'tipo': "familiar", 'confirmado': "SI"},
        {'id': 3, 'codigo': 'akosdjasd-1518', 'fecha': "15/03/2024", 'tipo': "familiar", 'confirmado': "NO"},
        {'id': 4, 'codigo': 'akosdjasd-1519', 'fecha': "15/03/2024", 'tipo': "chico/a", 'confirmado': "SI"},
        {'id': 5, 'codigo': 'akosdjasd-1520', 'fecha': "15/03/2024", 'tipo': "familiar", 'confirmado': "SI"},
        {'id': 6, 'codigo': 'akosdjasd-1521', 'fecha': "15/03/2024", 'tipo': "chico/a", 'confirmado': "SI"},
        {'id': 7, 'codigo': 'akosdjasd-1522', 'fecha': "15/03/2024", 'tipo': "familiar", 'confirmado': "SI"},
    ]

    contexto = {
        'cuestionarios': cuestionarios
    }

    return render(request, "home/index.html", contexto)
