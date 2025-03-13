from django.contrib import admin
from django.utils.timezone import now
from django.utils.html import format_html
from django.db.models import Q
from .models import Visitante, Visita, Setor

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'localizacao', 'get_horario_funcionamento', 'get_status_funcionamento')
    list_filter = ('tipo', 'localizacao')
    search_fields = ('nome',)

    def get_horario_funcionamento(self, obj):
        if obj.horario_abertura and obj.horario_fechamento:
            return f'{obj.horario_abertura.strftime("%H:%M")} - {obj.horario_fechamento.strftime("%H:%M")}'
        return 'Não definido'
    get_horario_funcionamento.short_description = 'Horário de Funcionamento'

    def get_status_funcionamento(self, obj):
        status = obj.status_funcionamento()
        if status == "Aberto":
            return format_html('<span style="color: #188038; font-weight: bold;">{}</span>', status)
        elif status == "Fechado":
            return format_html('<span style="color: #d93025; font-weight: bold;">{}</span>', status)
        return format_html('<span style="color: #666;">{}</span>', status)
    get_status_funcionamento.short_description = 'Status'

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'nome_social', 'CPF', 'data_nascimento')
    search_fields = ('nome_completo', 'nome_social', 'CPF')
    list_filter = ('bairro', 'cidade')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Se é um novo visitante
            # Cria automaticamente uma visita para o novo visitante
            Visita.objects.create(
                visitante=obj,
                data_entrada=now(),
                status='em_andamento'
            )

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'setor', 'objetivo', 'data_entrada', 'data_saida', 'status')
    list_filter = ('setor', 'objetivo', 'status', 'data_entrada')
    search_fields = ('visitante__nome_completo', 'visitante__CPF', 'setor__nome', 'objetivo', 'observacoes')
    date_hierarchy = 'data_entrada'

    fieldsets = (
        ('Visitante', {
            'fields': ('visitante',)
        }),
        ('Informações da Visita', {
            'fields': (
                'setor',
                'objetivo',
                'observacoes'
            )
        }),
        ('Status', {
            'fields': (
                'status',
                'data_entrada',
                'data_saida'
            )
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova visita
            obj.status = 'em_andamento'
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False  # Desabilita adição
    
    def has_change_permission(self, request, obj=None):
        return False  # Desabilita edição
    
    def has_delete_permission(self, request, obj=None):
        return False  # Desabilita exclusão

    def get_nome_visitante(self, obj):
        if obj.visitante:
            nome = obj.visitante.nome_completo
            if obj.visitante.nome_social:
                nome = f"{obj.visitante.nome_social} ({nome})"
            return format_html('<strong style="color: #333;">{}</strong>', nome)
        return format_html('<span style="color: red;">⚠️ Visitante não identificado</span>')
    get_nome_visitante.short_description = 'Nome do Visitante'
    get_nome_visitante.admin_order_field = 'visitante__nome_completo'

    def get_data_entrada(self, obj):
        return obj.data_entrada.strftime("%d/%m/%Y %H:%M")
    get_data_entrada.short_description = 'Data de Entrada'
    get_data_entrada.admin_order_field = 'data_entrada'

    def get_data_saida(self, obj):
        if obj.data_saida:
            return obj.data_saida.strftime("%d/%m/%Y %H:%M")
        return format_html('<span style="color: #28a745;">✓ Em andamento</span>')
    get_data_saida.short_description = 'Data de Saída'
    get_data_saida.admin_order_field = 'data_saida'

    def get_status(self, obj):
        if not obj.visitante:
            return format_html('<div class="status-sem-visita">⚠️ Erro: Sem Visitante</div>')
        if obj.status == 'finalizada':
            return format_html(
                '<div class="status-saida">'
                '🔴 Finalizada'
                '</div>'
            )
        elif obj.status == 'cancelada':
            return format_html(
                '<div class="status-cancelada">'
                '⚫ Cancelada'
                '</div>'
            )
        return format_html(
            '<div class="status-presente">'
            '🟢 Em Andamento'
            '</div>'
        )
    get_status.short_description = 'Status'

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }