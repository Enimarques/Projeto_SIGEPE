from django.contrib import admin
from django.utils.timezone import now
from django.utils.html import format_html
from django.db.models import Q
from .models import Visitante, Setor, Visita

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('get_nome_visitante', 'get_objetivo_visita', 'get_data_entrada', 'get_data_saida', 'get_status')
    search_fields = ('visitante__nome_completo', 'visitante__nome_social', 'visitante__CPF')
    list_filter = ('visitante__objetivo_visita', 'data_entrada', 'data_saida', 'status')
    
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

    def get_objetivo_visita(self, obj):
        if obj.visitante and obj.visitante.objetivo_visita:
            objetivo = dict(Visitante.OBJETIVO_CHOICES).get(obj.visitante.objetivo_visita, '')
            if obj.visitante.objetivo_visita == 'Outros' and obj.visitante.descricao_outros:
                objetivo = f"{objetivo} - {obj.visitante.descricao_outros}"
            return format_html('<span style="color: #666;">{}</span>', objetivo)
        return format_html('<span style="color: #999;">Não informado</span>')
    get_objetivo_visita.short_description = 'Objetivo da Visita'
    get_objetivo_visita.admin_order_field = 'visitante__objetivo_visita'

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

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('get_nome_completo', 'CPF', 'telefone', 'get_setor_display', 'get_objetivo_display', 'get_status_visita')
    search_fields = ('nome_completo', 'nome_social', 'CPF', 'telefone', 'cidade')
    list_filter = ('objetivo_visita', 'estado', 'cidade', 'setor__tipo', 'setor__is_vereador', 'visitas__status')
    
    def get_nome_completo(self, obj):
        if obj.nome_social:
            return format_html('<strong style="color: #333;">{}</strong> ({})', obj.nome_social, obj.nome_completo)
        return format_html('<strong style="color: #333;">{}</strong>', obj.nome_completo)
    get_nome_completo.short_description = 'Nome'
    get_nome_completo.admin_order_field = 'nome_completo'

    def get_objetivo_display(self, obj):
        if not obj.objetivo_visita:
            return format_html('<span style="color: #999;">Não informado</span>')
        objetivo = dict(Visitante.OBJETIVO_CHOICES).get(obj.objetivo_visita, 'Não informado')
        if obj.objetivo_visita == 'Outros' and obj.descricao_outros:
            objetivo = f"{objetivo} - {obj.descricao_outros}"
        return format_html('<span style="color: #666;">{}</span>', objetivo)
    get_objetivo_display.short_description = 'Objetivo da Visita'
    get_objetivo_display.admin_order_field = 'objetivo_visita'

    def get_setor_display(self, obj):
        if not obj.setor:
            return format_html('<span style="color: #999;">Não informado</span>')
        if obj.setor.is_vereador:
            return format_html('<strong style="color: #28a745;">Vereador(a) {}</strong>', obj.setor.nome)
        return format_html('<span style="color: #666;">{} - {}</span>', 
                         obj.setor.get_tipo_display(), obj.setor.nome)
    get_setor_display.short_description = 'Setor/Vereador'
    get_setor_display.admin_order_field = 'setor__nome'

    def get_status_visita(self, obj):
        # Busca a última visita do visitante
        ultima_visita = obj.visitas.order_by('-data_entrada').first()
        if not ultima_visita:
            return format_html('<div class="status-sem-visita">🔘 Sem visitas</div>')
        
        if ultima_visita.status == 'finalizada':
            return format_html(
                '<div class="status-saida">'
                '🔴 Visita finalizada em {}'
                '</div>',
                ultima_visita.data_saida.strftime("%d/%m/%Y %H:%M")
            )
        elif ultima_visita.status == 'cancelada':
            return format_html(
                '<div class="status-cancelada">'
                '⚫ Visita cancelada'
                '</div>'
            )
        return format_html(
            '<div class="status-presente">'
            '🟢 Visita em andamento desde {}'
            '</div>',
            ultima_visita.data_entrada.strftime("%d/%m/%Y %H:%M")
        )
    get_status_visita.short_description = 'Status da Visita'
    get_status_visita.admin_order_field = 'visitas__status'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Se é um novo visitante
            # Cria automaticamente uma visita para o novo visitante
            Visita.objects.create(
                visitante=obj,
                data_entrada=now(),
                status='em_andamento'
            )

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'nome_social', 'data_nascimento', 'CPF', 'foto')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Localização', {
            'fields': ('estado', 'cidade')
        }),
        ('Destino e Objetivo', {
            'fields': ('setor', 'objetivo_visita', 'descricao_outros')
        })
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "setor":
            kwargs["queryset"] = Setor.objects.all().order_by('tipo', 'nome')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_tipo_display', 'get_localizacao', 'is_vereador')
    list_filter = ('tipo', 'localizacao', 'is_vereador')
    search_fields = ('nome',)
    
    def get_tipo_display(self, obj):
        if obj.is_vereador:
            return format_html('<strong style="color: #28a745;">Gabinete de Vereador</strong>')
        return format_html('<span style="color: #666;">{}</span>', obj.get_tipo_display())
    get_tipo_display.short_description = 'Tipo'
    get_tipo_display.admin_order_field = 'tipo'
    
    def get_localizacao(self, obj):
        return format_html('<span style="color: #007bff;">{}</span>', obj.get_localizacao_display())
    get_localizacao.short_description = 'Localização'
    get_localizacao.admin_order_field = 'localizacao'

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo')
        }),
        ('Detalhes', {
            'fields': ('localizacao', 'is_vereador')
        })
    )

    def save_model(self, request, obj, form, change):
        if obj.tipo == 'gabinete_vereador':
            obj.is_vereador = True
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }