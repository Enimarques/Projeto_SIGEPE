"""
Módulo de administração para o app de veículos.
"""
# Importações absolutas para evitar problemas de importação
from django.contrib import admin
from .models import Veiculo

# Registrando o modelo Veiculo no admin
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'modelo', 'cor', 'visitante')
    search_fields = ('placa', 'modelo', 'visitante__nome')
    list_filter = ('tipo', 'cor')
