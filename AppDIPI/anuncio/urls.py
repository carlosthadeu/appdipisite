from django.urls import path, re_path
from .views import contato, lista_categoria, lista_categorias_adm, \
    exclui_categoria, nova_categoria, editar_categoria, lista_anuncio, \
    exclui_anuncio, editar_anuncio, novo_anuncio, lista_anunciante, \
    novo_anunciante, carregar_municipio_por_estado, excluir_anunciante, \
    editar_anunciante


app_name = 'anuncio'

urlpatterns = [
    path('formulario_contato', contato, name='contatoform'),
    # categoria no site
    re_path(r'^lst_categoria/(?P<slug>[\w_-]+)/$', lista_categoria, name='lista_categoria'),
    # categoria admin
    path('lst_categoria_adm', lista_categorias_adm, name='listagem_cat_adm'),
    path('lst_categoria_adm/exclui=<id>', exclui_categoria, name='exclui_categoria'),
    path('lst_categoria_adm/editar=<id>', editar_categoria, name='editar_categoria'),
    path('nova_categoria', nova_categoria, name='nova_categoria'),
    # anuncios
    path('lst_anuncio', lista_anuncio, name='listagem_anuncio'),
    path('lst_anuncio/exclui=<id>', exclui_anuncio, name='exclui_anuncio'),
    path('lst_anuncio/editar=<id>', editar_anuncio, name='editar_anuncio'),
    path('novo_anuncio', novo_anuncio, name='novo_anuncio'),
    # anunciantes
    path('lista_anunciante', lista_anunciante, name='listagem_anunciantes'),
    path('lista_anunciante/exclui=<id>', excluir_anunciante, name='excluir_anunciante'),
    path('lista_anunciante/editar=<id>', editar_anunciante, name='editar_anunciante'),
    path('novo_anunciante', novo_anunciante, name='novo_anunciante'),
    path('ajax/carregar-municipios/', carregar_municipio_por_estado, name='carregar_municipio_estado'),
]
