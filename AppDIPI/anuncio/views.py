from django.shortcuts import render, get_object_or_404
from .forms import EmailContato, PesquisaCategoria
from .models import Categoria, Anuncio, FotoAnuncio

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

def lista_categorias_adm(request):
    if (request.method == 'POST'):
        form = PesquisaCategoria(request.POST)
        if form.is_valid():
            pass
    else:
        context = context_cat_vazio()
    
    template_name = 'lista_categoria.html'
    return render(request, template_name, context)

def context_cat_vazio():
    context = {}
    form = PesquisaCategoria()
    lst_cat = Categoria.objects.all()
    context['lst_cat'] = lst_cat
    context['form'] = form
    context['excluido'] = False
    context['submetido'] = False
    return context

def exclui_categoria(request, id):
    pass