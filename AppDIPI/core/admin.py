from django.contrib import admin
from .models import Tela

# Register your models here.
class TelaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_field = ['nome']

admin.site.register(Tela, TelaAdmin)


