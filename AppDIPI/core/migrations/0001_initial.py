# Generated by Django 2.0.1 on 2020-03-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome da tela')),
                ('descricao', models.TextField(verbose_name='Descrição da tela')),
                ('tela', models.ImageField(upload_to='telas')),
                ('ordem', models.IntegerField(unique=True, verbose_name='Ordem de exibição')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Tela aplicativo',
                'verbose_name_plural': 'Telas do aplicativo',
                'ordering': ['nome'],
            },
        ),
    ]