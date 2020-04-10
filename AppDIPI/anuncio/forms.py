from django import forms
from django.forms import ModelForm
from django.conf import settings
from AppDIPI.core.email import send_mail_template
from django.forms.widgets import MultiWidget
from .models import Anuncio, TipoCategoria, Categoria
from django.forms.widgets import TextInput, Select, CheckboxInput
from  django.db.models.fields import TextField


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
    tipo = forms.ChoiceField(label='Tipo',choices=TipoCategoria.TIPO_CATEGORIA_CHOICES, 
        initial = TipoCategoria.SELECIONE, required=False,
        widget=Select(attrs={'class': 'form-control'}))
    nome = forms.CharField(label='Nome Categoria', max_length=100, strip=False, required=False, 
        widget= TextInput(attrs={'placeholder': 'Informe a categoria', 
        'class': 'form-control form-control-user'}) )
    
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'logo_categoria', 'tipo']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget = TextInput(attrs={
            'placeholder':'Nome da categoria',
            'class' : 'form-control form-control-user'},)
        
        self.fields['logo_categoria'].widget.attrs.update({'class': 'form-control-file'})
  
        self.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        
class AnuncioForm(ModelForm):
    class Meta:
        model : Anuncio
        fields = ['anunciante', 'apresentacao', 'endereco', 'telefone', 'categoria', 
        'email', 'instagram', 'facebook', 'youtube', 'site', 'slug', 'destaque']
    
    def __init__(self, *args, **kwargs):
        super(self).__init__(*args, **kwargs)
        for field in self.fields:
            if field is TextField:
                field.widget.attrs.update({'class': 'form-control form-control-user'})
    
class PesquisaAnuncio(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),empty_label='Selecione...',
        widget=Select(attrs={'class': 'form-control'}))

    anunciante = forms.CharField(label='Anunciante', max_length=100, strip=False, required=False, 
        widget= TextInput(attrs={'placeholder': 'Nome do anunciante', 
        'class': 'form-control form-control-user'}) )

    apresentacao = forms.CharField(label='Apresentação', max_length=100, strip=False, required=False, 
        widget= TextInput(attrs={'placeholder': 'Conteúdo do anúncio', 
        'class': 'form-control form-control-user'}) )
    
    ativo = forms.BooleanField(label='Ativo?', initial=True, widget=CheckboxInput(attrs={'class':'form-check-input'}))
