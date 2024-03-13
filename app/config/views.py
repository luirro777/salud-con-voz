from django.http import HttpResponse
from django.shortcuts import render

def home(request):


    cuestionarios = [
        {'id': 1, 'nombre': 'Javier', 'apellido': 'Martinez', 'dni': '22', 'edad': 31, 'resultado': 80},
        {'id': 2, 'nombre': 'Pedro', 'apellido': 'Gomez', 'dni': '23', 'edad': 31, 'resultado': 80},
        {'id': 3, 'nombre': 'Carolina', 'apellido': 'Carolinez', 'dni': '22', 'edad': 31, 'resultado': 80},
        {'id': 4, 'nombre': 'Pedro', 'apellido': 'Montagna', 'dni': '22', 'edad': 31, 'resultado': 80},
        {'id': 5, 'nombre': 'Martina', 'apellido': 'Aguilar', 'dni': '22', 'edad': 31, 'resultado': 80},
        {'id': 6, 'nombre': 'Josefa', 'apellido': 'Mirabella', 'dni': '22', 'edad': 31, 'resultado': 80},
        {'id': 7, 'nombre': 'Miguel', 'apellido': 'Torrez', 'dni': '22', 'edad': 31, 'resultado': 80},
    ]

    contexto = {
        'cuestionarios': cuestionarios
    }

    return render(request, "home/index.html", contexto)
