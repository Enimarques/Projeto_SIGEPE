from django.contrib import admin
from django.utils.timezone import now
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Q, Max
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from .models import Visitante, Visita, Setor, VisitanteArquivado, VisitaArquivada
from .forms_departamento import SetorForm
from .misc_utils import generate_password_token

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    form = SetorForm
    list_display = ('get_nome_display', 'tipo', 'localizacao', 'get_nome_responsavel', 'funcao', 'get_horario_trabalho', 'get_status_presenca', 'ativo', 'excluir_com_visitas')
    list_filter = ('tipo', 'localizacao', 'ativo')
    search_fields = ('nome_vereador', 'nome_local', 'nome_responsavel', 'email')
    ordering = ['tipo', 'nome_vereador', 'nome_local']
    readonly_fields = ('data_criacao', 'data_atualizacao')

    def get_fieldsets(self, request, obj=None):
        """Retorna fieldsets dinamicamente baseado no tipo do setor"""
        if obj and obj.tipo == 'gabinete':
            # Para gabinetes, não mostra o campo nome_responsavel
            return (
                ('Informações do Setor', {
                    'fields': ('tipo', 'localizacao', 'foto'),
                    'description': 'Informações básicas do setor'
                }),
                ('Informações do Gabinete', {
                    'fields': ('nome_vereador', 'email_vereador'),
                    'description': 'Informações do gabinete'
                }),
                ('Horário de Funcionamento', {
                    'fields': ('horario_abertura', 'horario_fechamento'),
                    'description': 'Defina o horário de funcionamento do setor'
                }),
                ('Informações do Assessor', {
                    'fields': ('funcao', 'email', 'horario_entrada', 'horario_saida'),
                    'description': 'Informações do assessor responsável'
                }),
                ('Status', {    
                    'fields': ('ativo',)
                }),
                ('Informações do Sistema', {
                    'fields': ('data_criacao', 'data_atualizacao'),
                    'classes': ('collapse',)
                })
            )
        else:
            # Para departamentos, mostra todos os campos
            if obj is None:
                # Formulário de adição: remove horário_entrada e horário_saida
                return (
                    ('Informações do Setor', {
                        'fields': ('tipo', 'localizacao', 'foto', 'nome_local', 'nome_vereador', 'email_vereador', 'horario_abertura', 'horario_fechamento'),
                        'description': 'Informações básicas do setor'
                    }),
                    ('Informações do Responsável', {
                        'fields': ('nome_responsavel', 'funcao', 'email'),
                        'description': 'Informações do responsável pelo departamento'
                    }),
                    ('Status', {    
                        'fields': ('ativo',)
                    }),
                    ('Informações do Sistema', {
                        'fields': ('data_criacao', 'data_atualizacao'),
                        'classes': ('collapse',)
                    })
                )
            else:
                return (
                    ('Informações do Setor', {
                        'fields': ('tipo', 'localizacao', 'foto', 'nome_local', 'horario_abertura', 'horario_fechamento'),
                        'description': 'Informações básicas do setor'
                    }),
                    ('Informações do Responsável', {
                        'fields': ('nome_responsavel', 'funcao', 'email', 'horario_entrada', 'horario_saida'),
                        'description': 'Informações do responsável pelo departamento'
                    }),
                    ('Status', {    
                        'fields': ('ativo',)
                    }),
                    ('Informações do Sistema', {
                        'fields': ('data_criacao', 'data_atualizacao'),
                        'classes': ('collapse',)
                    })
                )

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
        js = (
            'admin/js/jquery.init.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Só tenta acessar o campo se ele existir no form
        if obj and 'nome_responsavel' in form.base_fields:
            form.base_fields['nome_responsavel'].initial = obj.nome_responsavel
        return form

    def get_nome_display(self, obj):
        """Retorna o nome apropriado baseado no tipo do setor."""
        if obj.tipo == 'gabinete':
            return obj.nome_vereador or 'Gabinete sem nome'
        return obj.nome_local or 'Departamento sem nome'
    get_nome_display.short_description = 'Nome'

    def get_nome_responsavel(self, obj):
        """Retorna o nome do responsável de forma segura."""
        if obj.tipo == 'gabinete':
            return getattr(obj, 'nome_vereador', None) or 'Não definido'
        return getattr(obj, 'nome_responsavel', None) or 'Não definido'
    get_nome_responsavel.short_description = 'Responsável'

    def get_horario_trabalho(self, obj):
        """Retorna o horário de trabalho formatado."""
        if obj.horario_abertura and obj.horario_fechamento:
            return f"{obj.horario_abertura.strftime('%H:%M')} - {obj.horario_fechamento.strftime('%H:%M')}"
        return "Não definido"
    get_horario_trabalho.short_description = 'Horário de Funcionamento'

    def get_status_presenca(self, obj):
        """Retorna o status de presença do assessor."""
        return "Presente" if obj.ativo else "Ausente"
    get_status_presenca.short_description = 'Status'

    def excluir_com_visitas(self, obj):
        """Link para excluir o setor e suas visitas relacionadas (apenas superadmin)"""
        if obj and obj.id:
            url = reverse('recepcao:excluir_setor', args=[obj.id])
            return format_html(
                '<a href="{}" class="button" style="background-color: #ba2121; color: white; '
                'padding: 3px 8px; border-radius: 4px; text-decoration: none; font-size: 12px;">'
                '<i class="fas fa-trash"></i> Excluir (incl. visitas)</a>',
                url
            )
        return "-"
    excluir_com_visitas.short_description = 'Exclusão Avançada'




@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'CPF', 'telefone')
    search_fields = ('nome_completo', 'nome_social', 'CPF')
    list_filter = ('bairro', 'cidade')
    readonly_fields = ('data_cadastro', 'data_atualizacao')

    fieldsets = (
        ("Informações Pessoais", {
            'fields': ('nome_completo', 'nome_social', 'CPF', 'data_nascimento', 'telefone', 'email')
        }),
        ("Endereço", {
            'fields': ('logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'CEP'),
            'classes': ('collapse',)
        }),
        ("Foto", {
            'fields': ('foto',)
        }),
        ("Datas de Controle", {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo Visita."""
    list_display = (
        'visitante', 'setor', 'objetivo', 'data_entrada',
        'data_saida', 'status', 'duracao_formatada'
    )
    list_filter = ('setor', 'objetivo', 'status', 'data_entrada')
    search_fields = (
        'visitante__nome_completo', 'visitante__CPF',
        'setor__nome_vereador', 'setor__nome_local', 'objetivo', 'observacoes'
    )
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

    def duracao_formatada(self, obj):
        """Calcula e formata a duração da visita."""
        if obj.status == 'finalizada' and obj.data_saida:
            duracao = obj.data_saida - obj.data_entrada
            horas = duracao.seconds // 3600
            minutos = (duracao.seconds % 3600) // 60

            if horas > 0:
                return f"{horas}h {minutos}min"
            return f"{minutos} minutos"
        elif obj.status == 'em_andamento':
            duracao = timezone.now() - obj.data_entrada
            horas = duracao.seconds // 3600
            minutos = (duracao.seconds % 3600) // 60

            if horas > 0:
                return format_html(
                    '<span style="color: blue;">'
                    '{0}h {1}min (em andamento)</span>',
                    horas, minutos
                )
            return format_html(
                '<span style="color: blue;">'
                '{0} minutos (em andamento)</span>',
                minutos
            )
        return "-"
    duracao_formatada.short_description = 'Duração'

    def save_model(self, request, obj, form, change):
        """Salva o modelo no admin e atualiza datas e status."""
        if obj.status == 'finalizada' and not obj.data_saida:
            obj.data_saida = timezone.now()
        elif obj.status == 'em_andamento':
            obj.data_saida = None

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(
            pk__in=Visita.objects.values('pk').annotate(
                max_id=Max('pk')
            ).values('max_id')
        )
        return qs


@admin.register(VisitanteArquivado)
class VisitanteArquivadoAdmin(admin.ModelAdmin):
    """Admin para visitantes arquivados - apenas leitura para administradores"""
    list_display = ('nome_completo', 'CPF', 'data_arquivamento', 'usuario_arquivou', 'dias_restantes', 'num_visitas')
    list_filter = ('data_arquivamento', 'estado', 'cidade')
    search_fields = ('nome_completo', 'nome_social', 'CPF', 'email')
    readonly_fields = (
        'nome_completo', 'nome_social', 'data_nascimento', 'CPF', 'telefone', 'email',
        'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento', 'CEP',
        'foto', 'foto_thumbnail', 'foto_medium', 'foto_large', 'biometric_vector',
        'id_original', 'data_cadastro_original', 'data_arquivamento', 
        'usuario_arquivou', 'data_exclusao_definitiva'
    )
    date_hierarchy = 'data_arquivamento'
    
    fieldsets = (
        ("Informações Pessoais", {
            'fields': ('nome_completo', 'nome_social', 'CPF', 'data_nascimento', 'telefone', 'email')
        }),
        ("Endereço", {
            'fields': ('logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'CEP'),
            'classes': ('collapse',)
        }),
        ("Foto", {
            'fields': ('foto', 'foto_thumbnail', 'foto_medium', 'foto_large'),
            'classes': ('collapse',)
        }),
        ("Dados de Arquivamento", {
            'fields': (
                'id_original', 'data_cadastro_original', 'data_arquivamento', 
                'usuario_arquivou', 'data_exclusao_definitiva'
            )
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Não permite adicionar manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar
    
    def has_delete_permission(self, request, obj=None):
        # Apenas superusuários podem deletar (exclusão definitiva manual)
        return request.user.is_superuser
    
    def dias_restantes(self, obj):
        """Calcula dias restantes até expiração"""
        from datetime import timedelta
        from django.utils import timezone
        data_expiracao = obj.data_arquivamento + timedelta(days=180)
        dias = (data_expiracao - timezone.now()).days
        if dias <= 0:
            return format_html('<span style="color: red;">Expirado</span>')
        elif dias <= 30:
            return format_html('<span style="color: orange;">{} dias</span>', dias)
        return f"{dias} dias"
    dias_restantes.short_description = 'Dias Restantes'
    
    def num_visitas(self, obj):
        """Número de visitas arquivadas"""
        return obj.visitas_arquivadas.count()
    num_visitas.short_description = 'Visitas'


@admin.register(VisitaArquivada)
class VisitaArquivadaAdmin(admin.ModelAdmin):
    """Admin para visitas arquivadas - apenas leitura"""
    list_display = ('visitante_arquivado', 'nome_setor', 'data_entrada', 'data_saida', 'status', 'objetivo')
    list_filter = ('status', 'objetivo', 'localizacao', 'data_entrada')
    search_fields = (
        'visitante_arquivado__nome_completo', 'visitante_arquivado__CPF',
        'nome_setor', 'observacoes'
    )
    readonly_fields = (
        'visitante_arquivado', 'id_original', 'nome_setor', 'localizacao', 
        'objetivo', 'observacoes', 'data_entrada', 'data_saida', 'status', 
        'data_arquivamento'
    )
    date_hierarchy = 'data_entrada'
    
    fieldsets = (
        ('Visitante Arquivado', {
            'fields': ('visitante_arquivado',)
        }),
        ('Informações da Visita', {
            'fields': (
                'nome_setor',
                'objetivo',
                'localizacao',
                'observacoes'
            )
        }),
        ('Status e Datas', {
            'fields': (
                'status',
                'data_entrada',
                'data_saida'
            )
        }),
        ('Dados de Arquivamento', {
            'fields': ('id_original', 'data_arquivamento'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
