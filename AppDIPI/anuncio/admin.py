from django.contrib import admin

from .models import Categoria, Anuncio, FotoAnuncio

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'nome']
    search_fields = ['tipo', 'nome']
    prepopulated_fields = {'slug' : ('nome',)}

admin.site.register(Categoria, CategoriaAdmin)

class fotoInline(admin.TabularInline):
    def save_model(self, request, obj, form, change):
        if obj.principal:
            Anuncio.objects.filter(principal=True).exclude(pk=obj.pk).update(principal=False)
        super().save_model(request, obj, form, change)
    model = FotoAnuncio

class AnuncioAdmin(admin.ModelAdmin):
    inlines = [
        fotoInline,
    ]

    list_display = ['anunciante']
    search_fields = ['anunciante']
    prepopulated_fields = {'slug' : ('anunciante',)}

    


admin.site.register(Anuncio, AnuncioAdmin)
