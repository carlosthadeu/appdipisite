from django.shortcuts import render, get_object_or_404
from AppDIPI.anuncio.models import Categoria
from .models import Tela

# Create your views here.

def home(request):
    template_name = 'home.html'
    categoria_negocio = Categoria.objects.filter(tipo=1)
    context = {
        'categoria' : categoria_negocio
    }
    return render(request, template_name, context)

def telas(request):
    template_name = 'telas.html'
    telas = Tela.objects.all().order_by('ordem')
    context = {
        'telas' : telas
    }
    return render(request, template_name, context)


