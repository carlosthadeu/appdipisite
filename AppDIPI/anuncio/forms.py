from django import forms
from django.forms import ModelForm
from django.conf import settings
from AppDIPI.core.email import send_mail_template
from django.forms.widgets import MultiWidget
from .models import Anuncio, TipoCategoria, Categoria, Anunciante
from django.forms.widgets import TextInput, Select, CheckboxInput
from  django.forms import CharField
from AppDIPI.core.models import Municipios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.urls import reverse
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from AppDIPI.core.utils import CPF, Cnpj



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
        model = Anuncio
        fields = ['categoria', 'anunciante', 'titulo', 'apresentacao', 'destaque']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].widget.attrs.update({'class': 'form-control form-control-user'})
    
class PesquisaAnuncio(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),empty_label='Selecione...',
        widget=Select(attrs={'class': 'form-control'}))

    anunciante = forms.CharField(label='Anunciante', max_length=100, strip=False, required=False, 
        widget= TextInput(attrs={'placeholder': 'Pesquisar pelo nome do anunciante', 
        'class': 'form-control form-control-user'}) )

    apresentacao = forms.CharField(label='Apresentação', max_length=100, strip=False, required=False, 
        widget= TextInput(attrs={'placeholder': 'Pesquisar pelo conteúdo do anúncio', 
        'class': 'form-control form-control-user'}) )
    
    ativo = forms.BooleanField(label='Ativo?', initial=True, widget=CheckboxInput(attrs={'class':'form-check-input'}))

class AnuncianteForm(ModelForm):
    class Meta:
        model = Anunciante
        fields = ['nome', 'tipo_pessoa', 'cpf_cnpj', 'cep', 'logradouro', 'bairro', 
            'estado', 'cidade', 'email', 'instagram', 'facebook', 'youtube', 'site']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for key, field in self.fields.items():
        #    self.fields[key].widget.attrs.update({'class': 'form-control form-control-user'})
        self.helper = FormHelper()
        self.helper.form_id = 'anuncianteForm'
        self.helper.form_class = 'mt-3 mb-3'
        self.helper.form_method = 'post'
        # atributo do form para funcionar o ajax do município
        self.helper.attrs = {'data-municipio-url': reverse('anuncio:carregar_municipio_estado')}

        # Fieldsets
        self.helper.layout = Layout(
            TabHolder(
            Tab(
                'Principal',
                'nome',
                'tipo_pessoa',
                'cpf_cnpj'
            ),
            Tab(
                'Endereço',
                'cep',
                'logradouro',
                'bairro',
                'estado',
                'cidade'
            ),
            Tab(
                'Redes Sociais e Internet',
                'email',
                'instagram',
                'facebook',
                'youtube',
                'site'
            )
            ),
            FormActions(
                Submit('submit', 'Salvar'),
                Submit('cancel', 'Cancelar', css_class='btn-danger', formnovalidate='formnovalidate',)
            )
        )
           
        # Código abaixo faz parte dos procediemntos para viabilizar a escolha
        # dinâmica da cidade de acordo com o estado selecionado.
        self.fields['cidade'].queryset = Municipios.objects.none()
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Municipios.objects.filter(uf=estado_id)
            except (ValueError, TypeError):
                pass  
        #elif self.instance.pk:
        #    self.fields['cidade'].queryset = self.instance.estado.city_set.order_by('name')

    def clean_cpf_cnpj(self):
        data = self.cleaned_data['cpf_cnpj']
        tipo = self.cleaned_data['tipo_pessoa']
        if tipo == 1:
            cpf = CPF(data)
            if not cpf.isValid():
                raise forms.ValidationError("CPF inválido!")
        else:
            cnpj = Cnpj()
            if not cnpj.validate(data):
                raise forms.ValidationError("CNPJ inválido!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    
    
    
    
        


class PesquisarAnunciante(forms.Form):
    nome = forms.CharField(label='Nome do anunciante', required=False,  max_length=100,
        widget= TextInput(attrs={'placeholder': 'Pesquisar pelo nome do anunciante', 
        'class': 'form-control form-control-user'}) )
    
    cpf_cnpj = forms.CharField(label='CPF ou CNPJ', required=False, max_length=14,
        widget= TextInput(attrs={'placeholder': 'Pesquisar pelo CPF/CNPJ', 
        'class': 'form-control form-control-user'}) )