from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=150)
    logo_categoria = models.ImageField(upload_to='anuncios/logo_categoria')
    slug = models.SlugField('url', default='')
    tipo = models.IntegerField('Tipo de categoria', choices=TipoCategoria.TIPO_CATEGORIA_CHOICES, default=TipoCategoria.SELECIONE)

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


class Anuncio(models.Model):
    anunciante = models.CharField('Nome do anunciante', max_length=150, unique=True)
    apresentacao = models.TextField('Apresentação')
    endereco = models.CharField('Endereço', max_length=150)
    telefone = models.CharField('Telefone', max_length=11)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    email = models.EmailField('Email', null=True, blank=True)
    instagram = models.URLField('Instagram', null=True, blank=True)
    facebook = models.URLField('Facebook', null=True, blank=True)
    youtube = models.URLField('Youtube', null=True, blank=True)
    site = models.URLField('Site', null=True, blank=True)
    slug = models.SlugField('URL anúncio')
    destaque = models.BooleanField('Destaque?', default=False)
    ativo = models.BooleanField('Ativo?',default=True)

    def telefone_formatado(self):
        return '(%s%s) %s%s%s%s%s - %s%s%s%s' % tuple(self.telefone.zfill(11))

    def foto_principal(self):
        return self.fotos.get(principal=True).foto
    
    def foto_banner(self):
        return self.fotos.get(banner=True).foto

    def dsc_categoria(self):
        return self.categoria.nome
    
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'

    def __str__(self):
        return self.anunciante

class FotoAnuncio(models.Model):
    anuncio = models.ForeignKey(Anuncio, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='anuncios/foto_anuncio')
    principal = models.BooleanField('Principal', default=False)
    banner = models.BooleanField('Banner', default=False)
    class Meta:
        verbose_name = 'Foto do anúncio'
        verbose_name_plural = 'Fotos dos anúncios'