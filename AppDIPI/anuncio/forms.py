from django import forms
from django.conf import settings
from AppDIPI.core.email import send_mail_template
from django.forms.widgets import MultiWidget
from .models import Anuncio, tipo_categoria

class EmailContato(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
    telefone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'class':'form-control phone_mask'}))
    potencia = forms.CharField(label='Potência', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    nome_loja = forms.CharField(label='Nome da loja', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    numero_loja = forms.IntegerField(label='Número Loja', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)
    mensagem.widget.attrs.update({'class':'form-control'})

    def send_mail(self):
        subject = 'Contato solicitado através da página do aplicativo'
        context = {
            'nome': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'telefone': self.cleaned_data['telefone'],
            'potencia': self.cleaned_data['potencia'],
            'nome_loja': self.cleaned_data['nome_loja'],
            'numero_loja': self.cleaned_data['numero_loja'],
            'mensagem': self.cleaned_data['mensagem'],
        }
        template_name = 'email_contato.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )    

class PesquisaCategoria(forms.Form):
    tipo = forms.ChoiceField(label='Tipo',choices=tipo_categoria.TIPO_CATEGORIA_CHOICES, required=False)
    nome = forms.CharField(label='Nome Categoria', max_length=100, strip=False, required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Informe a categoria', 
        'class': 'form-control form-control-user'}) )



