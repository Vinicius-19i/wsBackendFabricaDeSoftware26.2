from django.contrib import admin

from .models import Fabricante, Componente


@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "pais_origem", "site")
    search_fields = ("nome",)


@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "tipo", "fabricante", "preco", "em_estoque")
    list_filter = ("tipo", "fabricante")
    search_fields = ("nome",)
