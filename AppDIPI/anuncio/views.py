from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import EmailContato, PesquisaCategoria, CategoriaForm, PesquisaAnuncio, AnuncioForm
from .models import Categoria, Anuncio, FotoAnuncio, TipoCategoria

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

def exclui_categoria(request, id):
    Categoria.objects.filter(pk=id).delete()
    context = context_cat_vazio()
    template_name = 'lista_categoria.html'
    messages.success(request, 'Categoria excluída com sucesso!', extra_tags='alert alert-success')
    return render(request, template_name, context)

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

# Anúncios

def lista_anuncio(request):
    template_name = 'lista_anuncio.html'
    context = context_anu_vazio()
    return render(request, template_name, context)

def novo_anuncio(request):
    pass

def context_anu_vazio():
    context = {}
    form = PesquisaAnuncio()
    lst_anu = Anuncio.objects.none()
    context['lst_anu'] = lst_anu
    context['form'] = form
    return context

def exclui_anuncio(request, id):
    pass

def editar_anuncio(request, id):
    pass