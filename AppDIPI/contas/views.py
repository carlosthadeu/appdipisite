from django.shortcuts import render
from .forms import criacao_usuario_form

# Create your views here.

def cria_usuario(request):
    template_name = 'cria_usuario.html'
    form = criacao_usuario_form()
    context = {
        'form':form
    }
    return render(request, template_name,context)


