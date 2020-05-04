from django.db import models


class UF():
    SELECIONE = None
    RO = 11
    AC = 12
    AM = 13
    RR = 14
    PA = 15
    AP = 16
    TO = 17
    MA = 21
    PI = 22
    CE = 23
    RN = 24
    PB = 25
    PE = 26
    AL = 27
    SE = 28
    BA = 29
    MG = 31
    ES = 32
    RJ = 33
    SP = 35
    PR = 41
    SC = 42
    RS = 43
    MS = 50
    MT = 51
    GO = 52
    DF = 53
    UF_CHOICES = [
        (SELECIONE, 'Selecione...'),
        (RO, 'Rondônia'),
        (AC, 'Acre'),
        (AM, 'Amazonas'),
        (RR, 'Roraima'),
        (PA, 'Pará'),
        (AP, 'Amapá'),
        (TO, 'Tocantins'),
        (MA, 'Maranhão'),
        (PI, 'Piauí'),
        (CE, 'Ceará'),
        (RN, 'Rio Grande do Norte'),
        (PB, 'Paraíba'),
        (PE, 'Pernambuco'),
        (AL, 'Alagoas'),
        (SE, 'Sergipe'),
        (BA, 'Bahia'),
        (MG, 'Minas Gerais'),
        (ES, 'Espírito Santo'),
        (RJ, 'Rio de Janeiro'),
        (SP, 'São Paulo'),
        (PR, 'Paraná'),
        (SC, 'Santa Catarina'),
        (RS, 'Rio Grande do Sul'),
        (MS, 'Mato Grosso do Sul'),
        (MT, 'Mato Grosso'),
        (GO, 'Goiás'),
        (DF, 'Distrito Federal'),
    ]

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

class Municipios(models.Model):
    codigo = models.CharField('Código IBGE', unique=True, null=False, blank=False, max_length=7)
    nome = models.CharField('Nome', null=False, blank=False, max_length=100)
    uf = models.IntegerField('UF', null=False, choices=UF.UF_CHOICES, default=UF.SELECIONE)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'
        ordering = ['codigo']

# Create your models here.
