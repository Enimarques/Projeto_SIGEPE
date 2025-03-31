"""
Módulo de administração para o app de recepção.
Contém as classes de administração para os modelos Assessor, Setor,
Visitante e Visita.
"""
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse

from apps.autenticacao.views_assessor import generate_password_token
from .models import Visitante, Visita, Setor, Assessor


@admin.register(Assessor)
class AssessorAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo Assessor."""
    list_display = (
        'nome', 'departamento', 'funcao', 'get_horario_trabalho',
        'get_status_presenca', 'usuario', 'ativo', 'get_link_senha'
    )
    list_filter = ('departamento', 'funcao', 'ativo')
    search_fields = ('nome', 'departamento__nome', 'email')
    ordering = ['nome']
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'departamento', 'funcao', 'email')
        }),
        ('Horário de Trabalho', {
            'fields': ('horario_entrada', 'horario_saida')
        }),
        ('Acesso ao Sistema', {
            'fields': ('usuario', 'ativo')
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def get_link_senha(self, obj):
        """Gera um link para definição de senha do assessor."""
        if obj and obj.id:
            token = generate_password_token(obj.id)
            url = reverse('autenticacao:set_password_assessor', args=[token])
            return format_html(
                '<a href="{}" class="button" target="_blank">'
                'Gerar Link para Definição de Senha</a>'
                '<div class="help">Clique para gerar um link que permite ao '
                'assessor definir sua senha.</div>',
                url
            )
        return "-"
    get_link_senha.short_description = 'Link para Definição de Senha'

    def get_queryset(self, request):
        """Personaliza a queryset para o admin."""
        self.request = request
        return super().get_queryset(request)

    def get_form(self, request, obj=None, **kwargs):
        """Personaliza o formulário para o admin."""
        form = super().get_form(request, obj, **kwargs)
        if 'departamento' in form.base_fields:
            # Limita os departamentos aos setores do tipo departamento
            form.base_fields['departamento'].queryset = (
                Setor.objects.filter(
                    tipo='departamento'
                )
            )
        return form

    def get_horario_trabalho(self, obj):
        """Retorna o horário de trabalho formatado."""
        if obj and obj.horario_entrada and obj.horario_saida:
            return (
                f"{obj.horario_entrada.strftime('%H:%M')} - "
                f"{obj.horario_saida.strftime('%H:%M')}"
            )
        return "-"
    get_horario_trabalho.short_description = 'Horário de Trabalho'

    def get_status_presenca(self, obj):
        """Retorna o status de presença do assessor."""
        if not obj or not obj.ativo:
            return format_html('<span style="color: #999;">Inativo</span>')

        if not hasattr(obj, 'horario_entrada') or not hasattr(obj, 'horario_saida'):
            return format_html('<span style="color: #999;">Horário não definido</span>')

        agora = timezone.localtime(timezone.now()).time()

        # Verifica se o horário atual está dentro do horário de trabalho
        if obj.horario_entrada <= agora <= obj.horario_saida:
            return format_html(
                '<span style="color: green; font-weight: bold;">'
                'Presente</span>'
            )
        return format_html('<span style="color: red;">Ausente</span>')
    get_status_presenca.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        """Salva o modelo no admin."""
        super().save_model(request, obj, form, change)


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo Setor."""
    list_display = (
        'nome', 'tipo', 'localizacao', 'get_horario_funcionamento',
        'get_status_funcionamento'
    )
    list_filter = ('tipo', 'localizacao')
    search_fields = ('nome',)

    def get_horario_funcionamento(self, obj):
        """Retorna o horário de funcionamento formatado."""
        return (
            f"{obj.horario_abertura.strftime('%H:%M')} - "
            f"{obj.horario_fechamento.strftime('%H:%M')}"
        )
    get_horario_funcionamento.short_description = 'Horário de Funcionamento'

    def get_status_funcionamento(self, obj):
        """Retorna o status de funcionamento do setor."""
        agora = timezone.localtime(timezone.now()).time()

        # Verifica se o horário atual está dentro do horário de funcionamento
        if obj.horario_abertura <= agora <= obj.horario_fechamento:
            return format_html(
                '<span style="color: green; font-weight: bold;">'
                'Aberto</span>'
            )
        return format_html('<span style="color: red;">Fechado</span>')
    get_status_funcionamento.short_description = 'Status'


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo Visitante."""
    list_display = (
        'nome_completo', 'nome_social', 'CPF', 'data_nascimento',
        'telefone', 'cidade', 'face_status'
    )
    list_filter = ('bairro', 'cidade', 'face_registrada')
    search_fields = ('nome_completo', 'nome_social', 'CPF', 'telefone')
    readonly_fields = ('face_registrada',)

    fieldsets = (
        ('Informações Pessoais', {
            'fields': (
                'nome_completo', 'nome_social', 'data_nascimento',
                'CPF', 'telefone', 'email'
            )
        }),
        ('Endereço', {
            'fields': ('estado', 'cidade', 'bairro')
        }),
        ('Reconhecimento Facial', {
            'fields': ('foto', 'face_registrada', 'face_id')
        }),
    )

    def face_status(self, obj):
        """Retorna o status de reconhecimento facial do visitante."""
        if obj.face_registrada:
            return format_html(
                '<span style="color: green; font-weight: bold;">'
                'Registrada</span>'
            )
        return format_html(
            '<span style="color: orange;">Não Registrada</span>'
        )
    face_status.short_description = 'Face'

    def save_model(self, request, obj, form, change):
        """Salva o modelo no admin."""
        super().save_model(request, obj, form, change)


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
        'setor__nome', 'objetivo', 'observacoes'
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

    class Media:
        """Classe para definir recursos de mídia para o admin."""
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
