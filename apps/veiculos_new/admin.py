from django.contrib import admin
from apps.veiculos_new.models import VeiculoTeste


class VeiculoTesteAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo VeiculoTeste."""
    list_display = ('nome',)
    search_fields = ('nome',)


# Registro explícito no admin
admin.site.register(VeiculoTeste, VeiculoTesteAdmin)
