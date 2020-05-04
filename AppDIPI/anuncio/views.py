from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import EmailContato, PesquisaCategoria, CategoriaForm, PesquisaAnuncio, \
    AnuncioForm, PesquisarAnunciante, AnuncianteForm
from .models import Categoria, Anuncio, FotoAnuncio, TipoCategoria, Anunciante
from django.contrib.auth.decorators import login_required
from AppDIPI.core.models import Municipios
from django.urls import reverse

# Create your views here.


def contato(request):
    template_name = 'contato.html'
    context = {}
    if request.method == 'POST':
        form = EmailContato(request.POST)
        if form.is_valid():
            context['valido'] = True
            form.send_mail()
            form = EmailContato()
    else:
        form = EmailContato()

    context['form'] = form

    return render(request, template_name, context)

def lista_categoria(request, slug):
    template_name = 'categoria.html'
    categoria = get_object_or_404(Categoria, slug=slug)
    anuncios = Anuncio.objects.filter(categoria=categoria)
    destaques = Anuncio.objects.filter(categoria=categoria, destaque=True)
    context = {
        'categoria' : categoria,
        'anuncios' : anuncios,
        'destaques' : destaques
    }

    return render(request, template_name, context)

# CADASTRO DE CATEGORIAS

@login_required
def lista_categorias_adm(request):
    template_name = 'lista_categoria.html'
    if (request.method == 'POST'):
        form = PesquisaCategoria(request.POST)
        if form.is_valid():
            if 'limpar' in request.POST:
                context = context_cat_vazio()
            else:
                nom_cat = form.cleaned_data['nome']
                tip_cat = form.cleaned_data['tipo']
                if nom_cat or tip_cat:
                    lst_cat = Categoria.objects.filter(tipo=tip_cat or tip_cat == TipoCategoria.SELECIONE, nome__icontains=nom_cat)
                else:
                    lst_cat = Categoria.objects.all()
                if lst_cat.count() == 0:
                    messages.info(request, 'Não há categoria cadastrada que atenda aos critérios da pesquisa!', extra_tags='alert alert-warning')
                context = {'lst_cat': lst_cat, 'form' : form}
    else:
        context = context_cat_vazio()
        
    return render(request, template_name, context)

@login_required
def nova_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!', extra_tags='alert alert-success')
            context = context_cat_vazio()            
            template_name = 'lista_categoria.html'
            return render(request, template_name, context)
    else:
        form = CategoriaForm()
    
    context = {'form' : form}
    template_name = 'cadastrar_categoria.html'
    return render(request, template_name, context)


def context_cat_vazio():
    context = {}
    form = PesquisaCategoria()
    lst_cat = Categoria.objects.all()
    context['lst_cat'] = lst_cat
    context['form'] = form
    return context

@login_required
def exclui_categoria(request, id):
    Categoria.objects.filter(pk=id).delete()
    context = context_cat_vazio()
    template_name = 'lista_categoria.html'
    messages.success(request, 'Categoria excluída com sucesso!', extra_tags='alert alert-success')
    return render(request, template_name, context)

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(data=request.POST or None , files=request.FILES or None, instance=categoria)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria alterada com sucesso!', extra_tags='alert alert-success')
            context = context_cat_vazio()            
            template_name = 'lista_categoria.html'
            return render(request, template_name, context)
    else:
        context = { 'form' : form}
        template_name = 'editar_categoria.html'
        return render(request, template_name, context)


# Anunciantes

@login_required
def lista_anunciante(request):
    template_name = 'anunciante/lista_anunciante.html'
    if (request.method == 'POST'):
        form = PesquisarAnunciante(request.POST)
        if form.is_valid():
            if 'limpar' in request.POST:
                context = context_anunciante_vazio()
            else:
                nom_anu = form.cleaned_data['nome']
                cpf_cnpj_anu = form.cleaned_data['cpf_cnpj']
                if nom_anu or cpf_cnpj_anu:
                    lst_anu = Anunciante.objects.filter(cpf_cnpj__icontains=cpf_cnpj_anu, nome__icontains=nom_anu)
                else:
                    lst_anu = Anunciante.objects.all()
                if lst_anu.count() == 0:
                    messages.info(request, 'Não há anunciantes cadastrados que atendam aos critérios da pesquisa!', extra_tags='alert alert-warning')
                context = {'lst_anu': lst_anu, 'form' : form}
    else:
        context = context_anunciante_vazio()
        
    return render(request, template_name, context)

def novo_anunciante(request):
    if request.method == 'POST':
        form = AnuncianteForm(request.POST)
        if 'cancel' in request.POST:
            url = reverse('anuncio:listagem_anunciantes')     # or e.g. reverse(self.get_success_url())
            return HttpResponseRedirect(url)
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Anunciante criado com sucesso!', extra_tags='alert alert-success')
                url = reverse('anuncio:listagem_anunciantes')
                return HttpResponseRedirect(url)
    else:
        form = AnuncianteForm()
    
    context = {'form' : form}
    template_name = 'anunciante/cadastrar_anunciante.html'
    return render(request, template_name, context)

def editar_anunciante(request, id):
    pass

def excluir_anunciante(request, id):
    Anunciante.objects.filter(pk=id).delete()
    messages.success(request, 'Anunciante excluído com sucesso!', extra_tags='alert alert-success')
    url = reverse('anuncio:listagem_anunciantes') 
    return HttpResponseRedirect(url)

def context_anunciante_vazio():
    context = {}
    form = PesquisarAnunciante()
    lst_anu = Anunciante.objects.none()
    context['lst_anu'] = lst_anu
    context['form'] = form
    return context

# Anúncios

@login_required
def lista_anuncio(request):
    pass

@login_required
def novo_anuncio(request):
    pass


def context_anu_vazio():
    context = {}
    form = PesquisaAnuncio()
    lst_anu = Anuncio.objects.none()
    context['lst_anu'] = lst_anu
    context['form'] = form
    return context

@login_required
def exclui_anuncio(request, id):
    pass

@login_required
def editar_anuncio(request, id):
    pass

# Ajax

def carregar_municipio_por_estado(request):
    estado = request.GET.get('estado')
    municipios = Municipios.objects.filter(uf=estado)
    template_name = 'anunciante/ajax_lista_municipio.html'
    context = {'municipios' : municipios}
    return render(request, template_name, context)