from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from AppDIPI.core.models import UF, Municipios

# Create your models here.

class TipoCategoria():
    SELECIONE = None
    NEGOCIOS = 1
    CLASSIFICADOS = 2
    TIPO_CATEGORIA_CHOICES = [
        (SELECIONE, 'Selecione...'),
        (NEGOCIOS, 'Negócio'),
        (CLASSIFICADOS, 'Classificado'),
    ]

class TipoPessoa():
    SELECIONE = None
    FISICA = 1
    JURIDICA = 2
    TIPO_PESSOA_CHOICES = [
        (SELECIONE, 'Selecione...'),
        (FISICA, 'Pessoa Física'),
        (JURIDICA, 'Pessoa Jurídica'),
    ]


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=150)
    logo_categoria = models.ImageField(upload_to='anuncios/logo_categoria')
    slug = models.SlugField('url', default='')
    tipo = models.IntegerField('Tipo de categoria', choices=TipoCategoria.TIPO_CATEGORIA_CHOICES, 
        default=TipoCategoria.SELECIONE)

    def get_absolute_url(self):
        return reverse('anuncio:lista_categoria', args=[str(self.slug)])

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        slug = slugify(self.get_tipo_display() + self.nome )
        self.slug = slug
        super(Categoria, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering=['nome']
        unique_together = ('tipo', 'nome')

class Anunciante(models.Model):
    nome = models.CharField('Nome do anunciante', max_length=150)
    tipo_pessoa = models.IntegerField('Tipo de pessoa', choices=TipoPessoa.TIPO_PESSOA_CHOICES, 
        default=TipoPessoa.SELECIONE, null=False)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=14, unique=True, blank=False, null=False)
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    logradouro = models.CharField('Logradouro', max_length=150, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=150, null=True, blank=True)
    estado = models.IntegerField('Estado', choices=UF.UF_CHOICES, null=True, blank=True)
    cidade = models.ForeignKey(Municipios, on_delete=models.CASCADE, null=True, blank=True)    
    email = models.EmailField('Email', null=True, blank=True)
    instagram = models.URLField('Instagram', null=True, blank=True)
    facebook = models.URLField('Facebook', null=True, blank=True)
    youtube = models.URLField('Youtube', null=True, blank=True)
    site = models.URLField('Site', null=True, blank=True)

    def cpf_cnpj_formatado(self):
        if self.tipo_pessoa == TipoPessoa.FISICA:
            str_formatado = '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple((self.cpf_cnpj).zfill(11))
        else:
            str_formatado = '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple((self.cpf_cnpj).zfill(14))
        return str_formatado

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Anunciante'
        verbose_name_plural = 'Anunciantes'
        ordering = ['nome']

class TelefoneAnunciante(models.Model):
    ddd = models.CharField('DDD', max_length=3)
    numero = models.CharField('Número', max_length=9)
    anunciante = models.ForeignKey(Anunciante, on_delete=models.CASCADE, related_name='telefones')

    def telefone_formatado(self):
        return '(%s%s) %s%s%s%s%s - %s%s%s%s' % tuple((self.ddd + self.telefone).zfill(11))


class Anuncio(models.Model):
    anunciante = models.ForeignKey(Anunciante, on_delete=models.CASCADE, related_name='anuncios')
    titulo = models.CharField('Título', max_length=150)
    apresentacao = models.TextField('Apresentação')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)    
    slug = models.SlugField('URL anúncio')
    destaque = models.BooleanField('Destaque?', default=False)
    ativo = models.BooleanField('Ativo?',default=True)    

    def foto_principal(self):
        return self.fotos.get(principal=True).foto
    
    def foto_banner(self):
        return self.fotos.get(banner=True).foto

    def __str__(self):
        return self.anunciante.nome + ' - ' + self.titulo
    
    def save(self, *args, **kwargs):
        slug = slugify(self.get_categoria_display() + ' ' + self.anunciante.id + ' ' + self.titulo )
        self.slug = slug
    
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['anunciante', 'titulo']
        unique_together = [('categoria', 'anunciante', 'titulo')]

    

class FotoAnuncio(models.Model):
    anuncio = models.ForeignKey(Anuncio, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='anuncios/foto_anuncio')
    principal = models.BooleanField('Principal', default=False)
    banner = models.BooleanField('Banner', default=False)
    class Meta:
        verbose_name = 'Foto do anúncio'
        verbose_name_plural = 'Fotos dos anúncios'