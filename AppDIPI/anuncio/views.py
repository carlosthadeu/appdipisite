from django.shortcuts import render, get_object_or_404
from .forms import EmailContato
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