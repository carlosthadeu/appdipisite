# Generated by Django 2.2.5 on 2020-04-21 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anunciante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome do anunciante')),
                ('tipo_pessoa', models.IntegerField(choices=[(None, 'Selecione...'), (1, 'Pessoa Física'), (2, 'Pessoa Jurídica')], default=None, verbose_name='Tipo de pessoa')),
                ('cpf_cnpj', models.CharField(max_length=14, verbose_name='CPF')),
                ('cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('logradouro', models.CharField(max_length=150, verbose_name='Logradouro')),
                ('bairro', models.CharField(max_length=150, verbose_name='Bairro')),
                ('estado', models.IntegerField(choices=[(None, 'Selecione...'), (11, 'Rondônia'), (12, 'Acre'), (13, 'Amazonas'), (14, 'Roraima'), (15, 'Pará'), (16, 'Amapá'), (17, 'Tocantins'), (21, 'Maranhão'), (22, 'Piauí'), (23, 'Ceará'), (24, 'Rio Grande do Norte'), (25, 'Paraíba'), (26, 'Pernambuco'), (27, 'Alagoas'), (28, 'Sergipe'), (29, 'Bahia'), (31, 'Minas Gerais'), (32, 'Espírito Santo'), (33, 'Rio de Janeiro'), (35, 'São Paulo'), (41, 'Paraná'), (42, 'Santa Catarina'), (43, 'Rio Grande do Sul'), (50, 'Mato Grosso do Sul'), (51, 'Mato Grosso'), (52, 'Goiás'), (53, 'Distrito Federal')], default=23, verbose_name='Estado')),
                ('cidade', models.CharField(default='Fortaleza', max_length=150, verbose_name='Cidade')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('instagram', models.URLField(blank=True, null=True, verbose_name='Instagram')),
                ('facebook', models.URLField(blank=True, null=True, verbose_name='Facebook')),
                ('youtube', models.URLField(blank=True, null=True, verbose_name='Youtube')),
                ('site', models.URLField(blank=True, null=True, verbose_name='Site')),
            ],
            options={
                'verbose_name': 'Anunciante',
                'verbose_name_plural': 'Anunciantes',
                'ordering': [('nome',)],
            },
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150, verbose_name='Título')),
                ('apresentacao', models.TextField(verbose_name='Apresentação')),
                ('slug', models.SlugField(verbose_name='URL anúncio')),
                ('destaque', models.BooleanField(default=False, verbose_name='Destaque?')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('anunciante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anuncios', to='anuncio.Anunciante')),
            ],
            options={
                'verbose_name': 'Anúncio',
                'verbose_name_plural': 'Anúncios',
                'ordering': ['anunciante', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='TelefoneAnunciante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ddd', models.CharField(max_length=3, verbose_name='DDD')),
                ('numero', models.CharField(max_length=9, verbose_name='Número')),
                ('anunciante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to='anuncio.Anunciante')),
            ],
        ),
        migrations.CreateModel(
            name='FotoAnuncio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='anuncios/foto_anuncio')),
                ('principal', models.BooleanField(default=False, verbose_name='Principal')),
                ('banner', models.BooleanField(default=False, verbose_name='Banner')),
                ('anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='anuncio.Anuncio')),
            ],
            options={
                'verbose_name': 'Foto do anúncio',
                'verbose_name_plural': 'Fotos dos anúncios',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome')),
                ('logo_categoria', models.ImageField(upload_to='anuncios/logo_categoria')),
                ('slug', models.SlugField(default='', verbose_name='url')),
                ('tipo', models.IntegerField(choices=[(None, 'Selecione...'), (1, 'Negócio'), (2, 'Classificado')], default=None, verbose_name='Tipo de categoria')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
                'unique_together': {('tipo', 'nome')},
            },
        ),
        migrations.AddField(
            model_name='anuncio',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anuncio.Categoria'),
        ),
        migrations.AlterUniqueTogether(
            name='anuncio',
            unique_together={('categoria', 'anunciante', 'titulo')},
        ),
    ]
