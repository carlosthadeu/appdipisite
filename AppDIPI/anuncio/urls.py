from django.urls import path, re_path
from .views import contato, lista_categoria, lista_categorias_adm, \
    exclui_categoria, nova_categoria, editar_categoria, lista_anuncio, \
    exclui_anuncio, editar_anuncio, novo_anuncio


app_name = 'anuncio'

urlpatterns = [
    path('formulario_contato', contato, name='contatoform'),
    re_path(r'^lst_categoria/(?P<slug>[\w_-]+)/$', lista_categoria, name='lista_categoria'),
    path('lst_categoria_adm', lista_categorias_adm, name='listagem_cat_adm'),
    path('lst_categoria_adm/exclui=<id>', exclui_categoria, name='exclui_categoria'),
    path('lst_categoria_adm/editar=<id>', editar_categoria, name='editar_categoria'),
    path('nova_categoria', nova_categoria, name='nova_categoria'),
    path('lst_anuncio', lista_anuncio, name='listagem_anuncio'),
    path('lst_anuncio/exclui=<id>', exclui_anuncio, name='exclui_anuncio'),
    path('lst_anuncio/editar=<id>', editar_anuncio, name='editar_anuncio'),
    path('novo_anuncio', novo_anuncio, name='novo_anuncio')
]
