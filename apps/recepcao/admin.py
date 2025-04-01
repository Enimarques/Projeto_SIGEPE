from django.contrib import admin
from django.utils.timezone import now
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Q, Max
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse
from .models import Visitante, Visita, Setor, Assessor

from apps.autenticacao.views_assessor import generate_password_token

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'localizacao', 'nome_responsavel', 'funcao', 'get_horario_trabalho', 'get_status_presenca', 'ativo')
    list_filter = ('tipo', 'localizacao', 'ativo')
    search_fields = ('nome', 'nome_responsavel', 'email')
    ordering = ['nome']
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações do Setor', {
            'fields': ('nome', 'tipo', 'localizacao')
        }),
        ('Horário de Funcionamento', {
            'fields': ('horario_abertura', 'horario_fechamento')
        }),
        ('Informações do Responsável', {
            'fields': ('nome_responsavel', 'funcao', 'email', 'horario_entrada', 'horario_saida')
        }),
        ('Status', {    
            'fields': ('ativo',)
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )

"""
Módulo de administração para o app de recepção.
Contém as classes de administração para os modelos Assessor, Setor,
Visitante e Visita.
"""

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
    
    def get_queryset(self, request):
        """Personaliza a queryset para o admin."""
        self.request = request
        return super().get_queryset(request)

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
        form = super().get_form(request, obj, **kwargs)
        if 'departamento' in form.base_fields:
            departamento_field = form.base_fields['departamento']
            old_widget = departamento_field.widget
            
            # Get the original widget from the RelatedFieldWidgetWrapper
            original_widget = getattr(old_widget, 'widget', old_widget)
            
            class CustomSelect(original_widget.__class__):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def render(self, name, value, attrs=None, renderer=None):
                    # Renderiza apenas o HTML do widget original
                    output = super().render(name, value, attrs, renderer)
                    
                    # Cria o script como uma string separada
                    script = f'''
                    <script type="text/javascript">
                        document.addEventListener('DOMContentLoaded', function() {{
                            // Função para atualizar os horários com base no departamento selecionado
                            function atualizarHorarios(departamentoId) {{
                                if (departamentoId) {{
                                    // Fazer uma requisição AJAX para obter os horários do departamento
                                    fetch('/admin/recepcao/setor/' + departamentoId + '/change/')
                                        .then(response => response.text())
                                        .then(html => {{
                                            // Criar um parser de DOM temporário
                                            const parser = new DOMParser();
                                            const doc = parser.parseFromString(html, 'text/html');
                                            
                                            // Extrair os horários do HTML retornado
                                            const horarioAbertura = doc.querySelector('#id_horario_abertura').value;
                                            const horarioFechamento = doc.querySelector('#id_horario_fechamento').value;
                                            
                                            // Atualizar os campos de horário do assessor
                                            const entrada = document.getElementById('id_horario_entrada');
                                            const saida = document.getElementById('id_horario_saida');
                                            
                                            if (horarioAbertura && (!entrada.value || entrada.getAttribute('data-auto-filled'))) {{
                                                entrada.value = horarioAbertura;
                                                entrada.setAttribute('data-auto-filled', 'true');
                                            }}
                                            
                                            if (horarioFechamento && (!saida.value || saida.getAttribute('data-auto-filled'))) {{
                                                saida.value = horarioFechamento;
                                                saida.setAttribute('data-auto-filled', 'true');
                                            }}
                                        }})
                                        .catch(error => console.error('Erro ao obter horários:', error));
                                }}
                            }}
                            
                            // Configurar o event listener para o campo de departamento
                            const departamentoSelect = document.getElementById('id_departamento');
                            if (departamentoSelect) {{
                                // Atualizar horários quando o departamento é alterado
                                departamentoSelect.addEventListener('change', function() {{
                                    atualizarHorarios(this.value);
                                }});
                                
                                // Atualizar horários no carregamento inicial se um departamento já estiver selecionado
                                if (departamentoSelect.value) {{
                                    atualizarHorarios(departamentoSelect.value);
                                }}
                            }}
                        }});
                    </script>
                    '''
                    
                    # Adiciona o script ao final do HTML do widget
                    from django.utils.safestring import mark_safe
                    output = mark_safe(output + script)
                    
                    # Adicionar script para preencher os campos imediatamente se o valor já estiver definido
                    if value:
                        try:
                            setor = Setor.objects.get(pk=value)
                            if setor.horario_abertura and setor.horario_fechamento:
                                script_imediato = f'''
                                <script type="text/javascript">
                                    document.addEventListener('DOMContentLoaded', function() {{
                                        var entrada = document.getElementById('id_horario_entrada');
                                        var saida = document.getElementById('id_horario_saida');
                                        if (!entrada.value) {{
                                            entrada.value = '{setor.horario_abertura.strftime("%H:%M")}';
                                            entrada.setAttribute('data-auto-filled', 'true');
                                        }}
                                        if (!saida.value) {{
                                            saida.value = '{setor.horario_fechamento.strftime("%H:%M")}';
                                            saida.setAttribute('data-auto-filled', 'true');
                                        }}
                                    }});
                                </script>
                                '''
                                output = mark_safe(output + script_imediato)
                        except Setor.DoesNotExist:
                            pass
                    return output
            
            # Create a custom widget based on the original widget
            custom_widget = CustomSelect(attrs=original_widget.attrs)
            
            # Wrap the custom widget with RelatedFieldWidgetWrapper
            departamento_field.widget = RelatedFieldWidgetWrapper(
                custom_widget,
                Assessor._meta.get_field('departamento').remote_field,
                self.admin_site,
                can_add_related=True
            )
        
        return form

    def get_horario_trabalho(self, obj):
        if obj.horario_entrada is None or obj.horario_saida is None:
            return 'Horário não definido'
        return f'{obj.horario_entrada.strftime("%H:%M")} - {obj.horario_saida.strftime("%H:%M")}'
    get_horario_trabalho.short_description = 'Horário de Trabalho'

    def get_status_presenca(self, obj):
        if obj.horario_entrada is None or obj.horario_saida is None:
            return format_html('<span style="color: #6c757d;">Horário não definido</span>')
        agora = timezone.localtime().time()
        if obj.horario_entrada <= agora <= obj.horario_saida:
            return format_html('<span style="color: #28a745;">✓ Presente</span>')
        return format_html('<span style="color: #dc3545;">✗ Ausente</span>')
    get_status_presenca.short_description = 'Status'

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
