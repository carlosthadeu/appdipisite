from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import criacao_usuario_form, pesquisa_usuario
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.list import ListView

# Create your views here.

def cria_usuario(request):
    if request.method == 'POST':
        form = criacao_usuario_form(request.POST)
        if form.is_valid():
            form.save()
            template_name = 'lista_usuarios.html'
            context = lst_usu_vazia()
            messages.success(request, 'Usuário criado com sucesso!', extra_tags='alert alert-success')
            return render(request, template_name, context)
    else:
        form = criacao_usuario_form()
        
    context = {
        'form' : form
        }    
    template_name = 'cria_usuario.html'
    return render(request, template_name, context)

def lista_usuarios(request, context={}):
    if request.method == 'POST':
        form = pesquisa_usuario(request.POST)        
        if form.is_valid():
            if 'limpar' in request.POST:
                context = lst_usu_vazia()
            else:
                nom_usu = form.cleaned_data['usuario']
                if nom_usu == '':
                    lst_usu = User.objects.all()
                else:
                    lst_usu = User.objects.filter(username__icontains=nom_usu)
                if lst_usu.count() == 0:
                    messages.info(request, 'Não há usuário cadastrado que atenda aos critérios da pesquisa!', extra_tags='alert alert-warning')
                context['lst_usu'] = lst_usu
                context['form'] = form
    else:
        context = lst_usu_vazia()

    template_name = 'lista_usuarios.html'
    return render(request, template_name, context)

def lst_usu_vazia():
    context = {}
    form = pesquisa_usuario()
    lst_usu = User.objects.all()
    context['lst_usu'] = lst_usu
    context['form'] = form
    return context

def exclui_usuario(request, id):
    User.objects.filter(pk=id).delete()
    context = lst_usu_vazia()   
    template_name = 'lista_usuarios.html'
    messages.success(request, 'Usuário excluído com sucesso!', extra_tags='alert alert-success')
    return render(request, template_name, context)

