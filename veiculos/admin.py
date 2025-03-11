from django.contrib import admin
from django.utils.html import format_html
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'tipo', 'cor', 'responsavel', 'get_status', 'horario_entrada', 'horario_saida')
    list_filter = ('status', 'tipo', 'cor', 'horario_entrada', 'horario_saida')
    search_fields = ('placa', 'modelo', 'responsavel')
    readonly_fields = ('status', 'horario_entrada')
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'modelo', 'tipo', 'cor')
        }),
        ('Responsável', {
            'fields': ('responsavel',)
        }),
        ('Controle de Horário', {
            'fields': ('horario_entrada', 'horario_saida', 'status')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    def get_status(self, obj):
        status_class = 'status-presente' if obj.status == 'presente' else 'status-saida'
        status_text = 'Presente' if obj.status == 'presente' else 'Saída Realizada'
        cor_class = f'cor-{obj.cor.lower()}'
        return format_html(
            '<div class="{} {}" style="padding: 8px; border-radius: 4px;">{}</div>',
            status_class, cor_class, status_text
        )
    get_status.short_description = 'Status'
    get_status.admin_order_field = 'status'

    def save_model(self, request, obj, form, change):
        if obj.horario_saida:
            obj.status = 'saida'
        else:
            obj.status = 'presente'
        super().save_model(request, obj, form, change)
