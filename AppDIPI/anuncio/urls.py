from django.urls import path, re_path
from .views import contato, lista_categoria

app_name = 'anuncio'

urlpatterns = [
    path('formulario_contato', contato, name='contatoform'),
    re_path(r'^lst_categoria/(?P<slug>[\w_-]+)/$', lista_categoria, name='lista_categoria'),
]
