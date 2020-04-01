from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import bs4_auth_form
from .views import cria_usuario


app_name = 'contas'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name= 'login.html', authentication_form = bs4_auth_form), name='login'),
    path('cria_usuario', cria_usuario, name='cria_usuario'),
]