from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User
from django import forms
from django.forms.widgets import TextInput, PasswordInput, Widget

class bs4_auth_form(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(
            attrs={
                'placeholder': 'Informe a senha',
                'class': 'form-control form-control-user'
            })
        
        self.fields['username'].widget = TextInput(
            attrs={
                'placeholder': 'Informe o usuário',
                'class': 'form-control form-control-user'
            })

class criacao_usuario_form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(
            attrs={
                'placeholder': 'Nova senha',
                'class': 'form-control form-control-user'
            })
        
        self.fields['password2'].widget = PasswordInput(
            attrs={
                'placeholder': 'Confirmar senha',
                'class': 'form-control form-control-user'
            })

        self.fields['username'].widget = TextInput(
            attrs={
                'placeholder': 'Informe o usuário',
                'class': 'form-control form-control-user'
            })
    
    