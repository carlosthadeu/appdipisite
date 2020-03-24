from django.db import models

class Tela(models.Model):
    nome = models.CharField('Nome da tela', max_length=100)
    descricao = models.TextField('Descrição da tela')
    tela = models.ImageField(upload_to='telas')
    ordem = models.IntegerField('Ordem de exibição', unique=True)
    slug = models.SlugField('slug')

    def nome_truncado(self):
        return self.nome.replace(' ','')

    class Meta:
        verbose_name = 'Tela aplicativo'
        verbose_name_plural = 'Telas do aplicativo'
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Create your models here.
