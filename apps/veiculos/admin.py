"""
Módulo de administração para o app de veículos.
"""
from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'cor', 'visitante', 'tipo', 'status', 'data_entrada', 'data_saida')
    list_filter = ('tipo', 'cor', 'status', 'data_entrada', 'data_saida')
    search_fields = ('placa', 'modelo', 'visitante__nome', 'observacoes')
    readonly_fields = ('status', 'data_entrada')
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'tipo', 'modelo', 'cor')
        }),
        ('Visitante', {
            'fields': ('visitante',)
        }),
        ('Registro', {
            'fields': ('data_entrada', 'data_saida', 'status', 'observacoes')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.data_saida:
            obj.status = 'saida'
        else:
            obj.status = 'presente'
        super().save_model(request, obj, form, change)
