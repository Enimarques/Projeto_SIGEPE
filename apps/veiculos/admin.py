"""
Módulo de administração para o app de veículos.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Veiculo, HistoricoVeiculo
from django.utils import timezone

@admin.register(HistoricoVeiculo)
class HistoricoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data_entrada', 'data_saida', 'visitante')
    list_filter = ('data_entrada', 'data_saida')
    search_fields = ('veiculo__placa', 'visitante__nome')
    readonly_fields = ('veiculo', 'data_entrada', 'data_saida', 'visitante')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'cor', 'visitante', 'tipo', 'status', 'data_entrada', 'data_saida', 'bloqueado_status')
    list_filter = ('tipo', 'cor', 'status', 'data_entrada', 'data_saida', 'bloqueado')
    search_fields = ('placa', 'modelo', 'visitante__nome', 'observacoes')
    readonly_fields = ('status', 'data_entrada')
    actions = ['exportar_para_excel', 'exportar_para_pdf', 'bloquear_veiculos', 'desbloquear_veiculos', 'registrar_saida']
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'tipo', 'modelo', 'cor', 'nome_condutor', 'nome_passageiro')
        }),
        ('Visitante', {
            'fields': ('visitante',)
        }),
        ('Registro', {
            'fields': ('data_entrada', 'data_saida', 'status', 'observacoes')
        }),
        ('Bloqueio', {
            'fields': ('bloqueado', 'motivo_bloqueio', 'data_bloqueio'),
            'classes': ('collapse',)
        }),
    )

    def bloquear_veiculos(self, request, queryset):
        for veiculo in queryset:
            veiculo.bloqueado = True
            veiculo.save()
        self.message_user(request, f"{queryset.count()} veículo(s) bloqueado(s) com sucesso.")
    bloquear_veiculos.short_description = "Bloquear veículos selecionados"

    def desbloquear_veiculos(self, request, queryset):
        for veiculo in queryset:
            veiculo.bloqueado = False
            veiculo.motivo_bloqueio = None
            veiculo.data_bloqueio = None
            veiculo.save()
        self.message_user(request, f"{queryset.count()} veículo(s) desbloqueado(s) com sucesso.")
    desbloquear_veiculos.short_description = "Desbloquear veículos selecionados"

    def bloqueado_status(self, obj):
        if obj.bloqueado:
            return format_html('<span style="color: red;">&#10060; Bloqueado</span>')
        return format_html('<span style="color: green;">&#10004; Liberado</span>')
    bloqueado_status.short_description = 'Status de Bloqueio'

    def exportar_para_excel(self, request, queryset):
        # Implementação da exportação para Excel
        pass
    exportar_para_excel.short_description = "Exportar para Excel"

    def exportar_para_pdf(self, request, queryset):
        # Implementação da exportação para PDF
        pass
    exportar_para_pdf.short_description = "Exportar para PDF"

    def save_model(self, request, obj, form, change):
        if obj.data_saida:
            obj.status = 'saida'
        elif obj.bloqueado:
            obj.status = 'bloqueado'
        else:
            obj.status = 'presente'
        super().save_model(request, obj, form, change)

@admin.action(description='Registrar saída dos veículos selecionados')
def registrar_saida(modeladmin, request, queryset):
    for veiculo in queryset:
        veiculo.data_saida = timezone.now()
        veiculo.save()
