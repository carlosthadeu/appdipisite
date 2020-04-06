from django.urls import path, re_path
from .views import contato, lista_categoria, lista_categorias_adm, exclui_categoria

app_name = 'anuncio'

urlpatterns = [
    path('formulario_contato', contato, name='contatoform'),
    re_path(r'^lst_categoria/(?P<slug>[\w_-]+)/$', lista_categoria, name='lista_categoria'),
    path('lst_categoria_adm', lista_categorias_adm, name='listagem_cat_adm'),
    path('lst_categoria_adm/exclui=<id>', exclui_categoria, name='exclui_categoria'),
]
