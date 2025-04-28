from django.shortcuts import render
from .models import Nivel

def inicio(request):
    return render(request, 'juegos/inicio.html')

def registro(request):
    return render(request, 'juegos/registro.html')

def login_view(request):
    return render(request, 'juegos/login.html')

def menu_view(request):
    return render(request, 'juegos/menu.html')

def niveles_view(request):
    return render(request, 'juegos/niveles.html')

