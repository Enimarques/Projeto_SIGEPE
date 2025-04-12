from django.contrib import admin
from django.utils.timezone import now
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Q, Max
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from .models import Visitante, Visita, Setor, Assessor
from .forms_departamento import SetorForm
from .utils import generate_password_token

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    form = SetorForm
    list_display = ('get_nome_display', 'tipo', 'localizacao', 'nome_responsavel', 'funcao', 'get_horario_trabalho', 'get_status_presenca', 'ativo', 'excluir_com_visitas')
    list_filter = ('tipo', 'localizacao', 'ativo')
    search_fields = ('nome_vereador', 'nome_local', 'nome_responsavel', 'email')
    ordering = ['tipo', 'nome_vereador', 'nome_local']
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações do Setor', {
            'fields': ('tipo', 'localizacao'),
            'description': 'Informações básicas do setor'
        }),
        ('Informações do Gabinete', {
            'fields': ('nome_vereador', 'email_vereador'),
            'description': 'Preencha apenas se o tipo for Gabinete',
            'classes': ('collapse',)
        }),
        ('Informações do Departamento', {
            'fields': ('nome_local',),
            'description': 'Preencha apenas se o tipo for Departamento',
            'classes': ('collapse',)
        }),
        ('Horário de Funcionamento', {
            'fields': ('horario_abertura', 'horario_fechamento'),
            'description': 'Defina o horário de funcionamento do setor'
        }),
        ('Informações do Responsável', {
            'fields': ('nome_responsavel', 'funcao', 'email', 'horario_entrada', 'horario_saida'),
            'description': 'Selecione um assessor cadastrado como responsável'
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
            'admin/js/setor.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['nome_responsavel'].initial = obj.nome_responsavel
        return form

    def get_nome_display(self, obj):
        """Retorna o nome apropriado baseado no tipo do setor."""
        if obj.tipo == 'GABINETE':
            return obj.nome_vereador
        return obj.nome_local
    get_nome_display.short_description = 'Nome'

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

@admin.register(Assessor)
class AssessorAdmin(admin.ModelAdmin):
    """Classe de administração para o modelo Assessor."""
    list_display = (
        'nome_responsavel', 'departamento', 'funcao', 'get_horario_trabalho',
        'get_status_presenca', 'ativo'
    )
    list_filter = ('ativo', 'departamento', 'funcao')
    search_fields = ('nome_responsavel', 'departamento__nome_vereador', 'departamento__nome_local', 'email')
    ordering = ['nome_responsavel']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_responsavel', 'departamento', 'funcao', 'email')
        }),
        ('Horário de Trabalho', {
            'fields': ('horario_entrada', 'horario_saida')
        }),
        ('Status', {
            'fields': ('ativo',)
        })
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

    def save_model(self, request, obj, form, change):
        """Salva o modelo no admin."""
        super().save_model(request, obj, form, change)


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'nome_social', 'CPF', 'data_nascimento')
    search_fields = ('nome_completo', 'nome_social', 'CPF')
    list_filter = ('bairro', 'cidade')
    readonly_fields = ('face_registrada', 'face_id')
    actions = ['excluir_com_historico']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Se é um novo visitante
            # Cria automaticamente uma visita para o novo visitante
            Visita.objects.create(
                visitante=obj,
                data_entrada=now(),
                status='em_andamento'
            )

    def has_delete_permission(self, request, obj=None):
        """
        Verifica se o usuário tem permissão para excluir um visitante.
        Superusuários sempre podem excluir, mesmo que o visitante tenha histórico.
        """
        # Se for superusuário, permite excluir qualquer visitante
        if request.user.is_superuser:
            return True
            
        # Para usuários normais, verifica se o visitante possui visitas
        if obj:
            visitas = Visita.objects.filter(visitante=obj)
            if visitas.exists():
                # Se o visitante tiver visitas, adiciona uma mensagem de erro (apenas uma vez)
                if not hasattr(request, '_visitante_delete_message_shown'):
                    messages.error(request, "Você não pode excluir este visitante porque ele possui histórico de visitas. Apenas administradores podem fazer isso.")
                    setattr(request, '_visitante_delete_message_shown', True)
                return False
                
        # Para usuários normais sem visitas ou sem obj específico, segue a permissão padrão
        return super().has_delete_permission(request, obj)

    def excluir_com_historico(self, request, queryset):
        """
        Ação personalizada para excluir visitantes mesmo que tenham histórico de visitas.
        Esta ação exclui primeiro todas as visitas associadas e depois o visitante.
        """
        if not request.user.is_superuser:
            self.message_user(
                request,
                "Apenas superusuários podem excluir visitantes com histórico de visitas.",
                level=messages.ERROR
            )
            return

        visitantes_excluidos = 0
        visitas_excluidas = 0
        erros = 0

        for visitante in queryset:
            try:
                with transaction.atomic():
                    # Conta e exclui as visitas associadas
                    visitas = Visita.objects.filter(visitante=visitante)
                    num_visitas = visitas.count()
                    visitas.delete()
                    visitas_excluidas += num_visitas
                    
                    # Exclui o visitante
                    nome_visitante = visitante.nome_completo
                    visitante.delete()
                    visitantes_excluidos += 1
            except Exception as e:
                erros += 1
                self.message_user(
                    request,
                    f"Erro ao excluir {visitante.nome_completo}: {str(e)}",
                    level=messages.ERROR
                )

        if visitantes_excluidos > 0:
            self.message_user(
                request,
                f"{visitantes_excluidos} visitante(s) e {visitas_excluidas} visita(s) excluídos com sucesso.",
                level=messages.SUCCESS
            )
        
        if erros > 0:
            self.message_user(
                request,
                f"{erros} visitante(s) não puderam ser excluídos. Verifique os erros acima.",
                level=messages.WARNING
            )
    
    excluir_com_historico.short_description = "Excluir visitantes selecionados e seu histórico de visitas"

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
