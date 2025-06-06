from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Visitante, Visita, Setor, Assessor
from .forms import VisitanteForm, VisitaForm
from .forms_departamento import SetorForm
from .utils import gerar_etiqueta_pdf
import base64
import json
from django.urls import reverse
from datetime import datetime, timedelta
from .forms_departamento import AlterarHorarioSetorForm
from django.core.exceptions import PermissionDenied
from apps.autenticacao.decorators import admin_required
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.template.loader import render_to_string
from apps.veiculos.models import Veiculo

# Contexto base para todas as views do app
def get_base_context(title_suffix=''):
    return {
        'title': f'Recepção - {title_suffix}' if title_suffix else 'Recepção - URUTAU',
        'app_name': 'recepcao'
    }

@login_required(login_url='autenticacao:login_sistema')
def home_recepcao(request):
    hoje = timezone.localtime().date()
    
    # Contagem de visitas
    visitas_hoje = Visita.objects.filter(data_entrada__date=hoje).count()
    visitas_em_andamento = Visita.objects.filter(data_saida__isnull=True).count()
    visitas_finalizadas_hoje = Visita.objects.filter(data_entrada__date=hoje, data_saida__isnull=False).count()
    total_visitantes = Visitante.objects.count()
    
    # Contagem de veículos
    veiculos_no_estacionamento = Veiculo.objects.filter(status='presente').count()
    total_veiculos_cadastrados = Veiculo.objects.count()
    
    context = get_base_context()
    context.update({
        'visitas_hoje': visitas_hoje,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas_hoje': visitas_finalizadas_hoje,
        'total_visitantes': total_visitantes,
        'veiculos_no_estacionamento': veiculos_no_estacionamento,
        'total_veiculos_cadastrados': total_veiculos_cadastrados
    })
    return render(request, 'recepcao/home_recepcao.html', context)

@login_required(login_url='autenticacao:login_sistema')
def lista_visitantes(request):
    # Obter parâmetros de busca
    busca = request.GET.get('busca', '')
    
    # Query base
    visitantes = Visitante.objects.all()
    
    # Aplicar filtro de busca
    if busca:
        visitantes = visitantes.filter(
            Q(nome_completo__icontains=busca) |
            Q(CPF__icontains=busca) |
            Q(email__icontains=busca)
        )
    
    # Ordenar por nome
    visitantes = visitantes.order_by('nome_completo')
    
    context = get_base_context('Lista de Visitantes')
    context.update({
        'visitantes': visitantes,
        'busca': busca
    })
    
    return render(request, 'recepcao/lista_visitantes.html', context)

@login_required(login_url='autenticacao:login_sistema')
def cadastro_visitantes(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST, request.FILES)
        if form.is_valid():
            visitante = form.save()
            messages.success(request, 'Visitante cadastrado com sucesso!')
            return redirect('recepcao:detalhes_visitante', pk=visitante.id)
    else:
        form = VisitanteForm()
    
    context = get_base_context('Cadastro de Visitante')
    context.update({
        'form': form,
        'visitante': None,  
    })
    
    return render(request, 'recepcao/cadastro_visitantes.html', context)

@login_required(login_url='autenticacao:login_sistema')
def detalhes_visitante(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    
    # Obter todas as visitas relacionadas a este visitante
    visitas = Visita.objects.filter(visitante=visitante).order_by('-data_entrada')
    
    context = get_base_context('Detalhes do Visitante')
    context.update({
        'visitante': visitante,
        'visitas': visitas
    })
    return render(request, 'recepcao/detalhes_visitante.html', context)

@login_required(login_url='autenticacao:login_sistema')
def editar_visitante(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    
    if request.method == 'POST':
        form = VisitanteForm(request.POST, request.FILES, instance=visitante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visitante atualizado com sucesso!')
            return redirect('recepcao:lista_visitantes')
    else:
        # Formatando a data para o formato esperado pelo campo
        if visitante.data_nascimento:
            visitante.data_nascimento = visitante.data_nascimento.strftime('%Y-%m-%d')
        form = VisitanteForm(instance=visitante)
    
    context = get_base_context('Editar Visitante')
    context.update({
        'form': form,
        'visitante': visitante,
        'is_editing': True
    })
    
    return render(request, 'recepcao/cadastro_visitantes.html', context)

@login_required(login_url='autenticacao:login_sistema')
def registro_visitas(request):
    # Verificar se tem visitante pré-selecionado
    visitante_id = request.GET.get('visitante')
    visitante = None
    if visitante_id:
        try:
            visitante = Visitante.objects.get(id=visitante_id)
        except Visitante.DoesNotExist:
            messages.error(request, 'Visitante não encontrado.')
    
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            try:
                visitante = Visitante.objects.get(CPF=form.cleaned_data['cpf'])
                setor = form.cleaned_data['setor']
                
                # Criar a visita
                visita = Visita.objects.create(
                    visitante=visitante,
                    setor=setor,
                    objetivo=form.cleaned_data['objetivo'],
                    observacoes=form.cleaned_data.get('observacoes', ''),
                    localizacao=setor.localizacao  # Usando a localização do setor
                )
                
                messages.success(request, 'Visita registrada com sucesso!')
                return redirect('recepcao:status_visita')
            except Visitante.DoesNotExist:
                messages.error(request, 'Visitante não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao registrar visita: {str(e)}')
    else:
        initial_data = {}
        if visitante:
            initial_data['cpf'] = visitante.CPF
        form = VisitaForm(initial=initial_data)
    
    context = get_base_context('Registro de Visitas')
    context.update({
        'form': form,
        'visitante_pre_selecionado': visitante
    })
    
    return render(request, 'recepcao/registro_visitas.html', context)

@login_required(login_url='autenticacao:login_sistema')
def buscar_visitante(request):
    query = request.GET.get('query', None)
    
    if not query or len(query) < 3:
        return JsonResponse({'success': False, 'message': 'Digite ao menos 3 caracteres para buscar.'})
    
    # Limpa o CPF de formatação para a busca no banco
    cleaned_query = query.replace('.', '').replace('-', '')
    
    # Busca por nome ou por CPF
    visitantes = Visitante.objects.filter(
        Q(nome_completo__icontains=query) |
        Q(CPF__icontains=cleaned_query)
    ).order_by('nome_completo')[:10] # Limita a 10 resultados

    if not visitantes.exists():
        return JsonResponse({
            'success': False,
            'message': 'Nenhum visitante encontrado.'
        })

    # Prepara os dados para a resposta JSON
    visitantes_data = []
    for v in visitantes:
        # Buscar a última visita do visitante
        ultima_visita = Visita.objects.filter(visitante=v).order_by('-data_entrada').first()
        
        visitante_data = {
            'id': v.id,
            'nome_completo': v.nome_completo,
            'cpf': v.CPF, # Retorna o CPF formatado
            'telefone': v.telefone,
            'foto': v.foto.url if v.foto else None,
            'ultima_visita': ultima_visita.data_entrada.strftime('%d/%m/%Y') if ultima_visita else None,
            'total_visitas': Visita.objects.filter(visitante=v).count(),
            'email': v.email if v.email else 'Não informado'
        }
        visitantes_data.append(visitante_data)

    return JsonResponse({'success': True, 'visitantes': visitantes_data})

@login_required(login_url='autenticacao:login_sistema')
def buscar_setores(request):
    tipo = request.GET.get('tipo', 'departamento')
    
    # Filtrar setores por tipo
    setores = Setor.objects.filter(tipo=tipo).order_by('nome_vereador', 'nome_local')
    
    if not setores.exists():
        return JsonResponse({
            'success': False,
            'message': f'Nenhum {tipo} encontrado.'
        })
    
    # Preparar dados dos setores
    setores_data = []
    for setor in setores:
        setores_data.append({
            'id': setor.id,
            'tipo': setor.tipo,
            'nome_vereador': setor.nome_vereador if setor.tipo == 'gabinete' else None,
            'nome_local': setor.nome_local if setor.tipo == 'departamento' else None,
            'localizacao': setor.get_localizacao_display()
        })
    
    return JsonResponse({
        'success': True,
        'setores': setores_data
    })

@login_required(login_url='autenticacao:login_sistema')
def historico_visitas(request):
    # Filtros
    status = request.GET.get('status')
    periodo = request.GET.get('periodo')
    busca = request.GET.get('busca')
    
    # Query base
    visitas = Visita.objects.all()
    print(f"Total de visitas antes dos filtros: {visitas.count()}")
    
    # Aplicar filtros
    if status:
        print(f"Aplicando filtro de status: {status}")
        if status == 'em_andamento':
            visitas = visitas.filter(data_saida__isnull=True)
        elif status == 'finalizada':
            visitas = visitas.filter(data_saida__isnull=False)
        print(f"Total após filtro de status: {visitas.count()}")
    
    if periodo:
        print(f"Aplicando filtro de período: {periodo}")
        hoje = timezone.localtime().date()
        if periodo == 'hoje':
            visitas = visitas.filter(data_entrada__date=hoje)
        elif periodo == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            visitas = visitas.filter(data_entrada__date__gte=inicio_semana)
        elif periodo == 'mes':
            inicio_mes = hoje.replace(day=1)
            visitas = visitas.filter(data_entrada__date__gte=inicio_mes)
        print(f"Total após filtro de período: {visitas.count()}")
    
    if busca:
        print(f"Aplicando busca: {busca}")
        visitas = visitas.filter(
            Q(visitante__nome_completo__icontains=busca) |
            Q(visitante__CPF__icontains=busca)
        )
        print(f"Total após busca: {visitas.count()}")
    
    # Ordenação
    visitas = visitas.order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(visitas, 10)  # 10 visitas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_visitas = visitas.count()
    visitas_em_andamento = visitas.filter(data_saida__isnull=True).count()
    visitas_finalizadas = visitas.filter(data_saida__isnull=False).count()
    
    context = get_base_context('Histórico de Visitas')
    context.update({
        'page_obj': page_obj,
        'total_visitas': total_visitas,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas': visitas_finalizadas,
        # Manter filtros selecionados
        'status_filtro': status,
        'periodo_filtro': periodo,
        'busca': busca,
    })
    
    return render(request, 'recepcao/historico_visitas.html', context)

@login_required(login_url='autenticacao:login_sistema')
def status_visita(request):
    """
    Exibe as visitas em andamento com filtros.
    """
    # Obter parâmetros do filtro
    data = request.GET.get('data')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    localizacao = request.GET.get('localizacao')
    setor = request.GET.get('setor')

    # Iniciar queryset com visitas não finalizadas e status em andamento
    visitas = Visita.objects.filter(
        data_saida__isnull=True,
        status='em_andamento'
    )

    # Aplicar filtros
    if data:
        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
            visitas = visitas.filter(data_entrada__date=data)
        except (ValueError, TypeError):
            messages.error(request, 'Data inválida')

    if hora_inicio:
        try:
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            visitas = visitas.filter(data_entrada__time__gte=hora_inicio)
        except (ValueError, TypeError):
            messages.error(request, 'Hora de início inválida')

    if hora_fim:
        try:
            hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
            visitas = visitas.filter(data_entrada__time__lte=hora_fim)
        except (ValueError, TypeError):
            messages.error(request, 'Hora de fim inválida')

    if localizacao:
        visitas = visitas.filter(localizacao=localizacao)

    if setor:
        visitas = visitas.filter(setor_id=setor)

    # Ordenar por data de entrada mais recente
    visitas = visitas.order_by('-data_entrada')

    # Estatísticas principais para os cards conforme modelo de referência
    total_em_andamento = visitas.count()
    total_visitantes = Visitante.objects.count()
    
    # Métricas de veículos
    veiculos_no_estacionamento = Veiculo.objects.filter(
        status='presente'
    ).count()
    total_veiculos_cadastrados = Veiculo.objects.count()
    
    # Estatísticas por localização (para gráficos ou outras visualizações se necessário)
    total_por_local = {
        'terreo': visitas.filter(localizacao='terreo').count(),
        'plenario': visitas.filter(localizacao='plenario').count(),
        'primeiro_piso': visitas.filter(localizacao='primeiro_piso').count(),
        'segundo_piso': visitas.filter(localizacao='segundo_piso').count()
    }

    context = get_base_context('Status das Visitas')
    context.update({
        'visitas': visitas,
        'total_em_andamento': total_em_andamento,
        'total_visitantes': total_visitantes,
        'veiculos_no_estacionamento': veiculos_no_estacionamento,
        'total_veiculos_cadastrados': total_veiculos_cadastrados,
        'total_por_local': total_por_local,
        'setores': Setor.objects.filter(ativo=True).order_by('nome_vereador', 'nome_local'),
        'localizacoes': dict(Visita.LOCALIZACAO_CHOICES),
        # Manter filtros selecionados
        'data_filtro': data if data else None,
        'hora_inicio_filtro': hora_inicio.strftime('%H:%M') if hora_inicio else '',
        'hora_fim_filtro': hora_fim.strftime('%H:%M') if hora_fim else '',
        'localizacao_filtro': localizacao,
        'setor_filtro': setor
    })

    return render(request, 'recepcao/status_visita.html', context)

@login_required(login_url='autenticacao:login_sistema')
def finalizar_visita(request, visita_id):
    """
    Finaliza uma visita em andamento.
    """
    try:
        visita = Visita.objects.get(id=visita_id)
    except Visita.DoesNotExist:
        messages.error(request, 'Visita não encontrada. Ela pode ter sido finalizada ou excluída por outro usuário.')
        return redirect('recepcao:status_visita')
    
    # Verificar a URL de origem para saber para onde redirecionar depois
    referrer = request.META.get('HTTP_REFERER', '')
    
    # Verifica se a visita já foi finalizada
    if visita.data_saida or visita.status != 'em_andamento':
        messages.error(request, 'Esta visita já foi finalizada.')
        # Redirecionar para a página de origem
        if 'historico' in referrer:
            return redirect('recepcao:historico_visitas')
        elif 'detalhes_visitante' in referrer:
            return redirect('recepcao:detalhes_visitante', pk=visita.visitante.id)
        else:
            return redirect('recepcao:status_visita')
    
    try:
        # Finaliza a visita
        visita.data_saida = timezone.now()
        visita.status = 'finalizada'
        visita.save()
        
        messages.success(request, 'Visita finalizada com sucesso!')
        
        # Redirecionar para a página de origem
        if 'historico' in referrer:
            return redirect('recepcao:historico_visitas')
        elif 'detalhes_visitante' in referrer:
            return redirect('recepcao:detalhes_visitante', pk=visita.visitante.id)
        else:
            return redirect('recepcao:status_visita')
    except Exception as e:
        messages.error(request, f'Erro ao finalizar visita: {str(e)}')
        return redirect('recepcao:status_visita')

@login_required(login_url='autenticacao:login_sistema')
@admin_required
def excluir_visita(request, pk):
    visita = get_object_or_404(Visita, pk=pk)
    visita.delete()
    messages.success(request, 'Visita excluída com sucesso!')
    return redirect('recepcao:historico_visitas')

@login_required(login_url='autenticacao:login_sistema')
def excluir_setor(request, pk):
    # Verificar se o usuário é superadmin
    if not request.user.is_superuser:
        messages.error(request, 'Apenas administradores podem excluir setores.')
        return redirect('admin:recepcao_setor_changelist')
        
    setor = get_object_or_404(Setor, pk=pk)
    
    if request.method == 'POST':
        try:
            # Excluir todas as visitas relacionadas a este setor
            visitas_relacionadas = Visita.objects.filter(setor=setor)
            qtd_visitas = visitas_relacionadas.count()
            
            # Excluir as visitas primeiro
            if qtd_visitas > 0:
                visitas_relacionadas.delete()
                messages.warning(request, f'{qtd_visitas} visita(s) relacionada(s) foram excluída(s).')
            
            # Verificar se o setor está relacionado a um gabinete
            try:
                from apps.gabinetes.models import Gabinete
                gabinetes = Gabinete.objects.filter(setor=setor)
                if gabinetes.exists():
                    # Excluir os gabinetes relacionados
                    qtd_gabinetes = gabinetes.count()
                    gabinetes.delete()
                    messages.warning(request, f'{qtd_gabinetes} gabinete(s) relacionado(s) foram excluído(s).')
            except ImportError:
                pass
                
            # Verificar se existem assessores relacionados ao setor
            assessores = Assessor.objects.filter(
                ativo=True,
                departamento__isnull=False
            ).order_by('nome_vereador', 'nome_local')
            if assessores.exists():
                # Desassociar os assessores deste setor
                qtd_assessores = assessores.count()
                assessores.update(departamento=None)
                messages.warning(request, f'{qtd_assessores} assessor(es) relacionado(s) foram desassociados.')
                
            # Depois excluir o setor
            nome_setor = setor.nome_vereador if setor.tipo == 'gabinete' else setor.nome_local
            setor.delete()
            messages.success(request, f'Setor "{nome_setor}" excluído com sucesso!')
            
            # Redirecionar para a lista de setores no admin
            return redirect('admin:recepcao_setor_changelist')
        except Exception as e:
            messages.error(request, f"Erro ao excluir setor: {str(e)}")
            return redirect('admin:recepcao_setor_changelist')
    
    # Mostra um template de confirmação
    context = {
        'setor': setor,
        'visitas_relacionadas': Visita.objects.filter(setor=setor),
        'objeto_tipo': 'Setor',
        'objeto_nome': setor.nome_vereador if setor.tipo == 'gabinete' else setor.nome_local
    }
    
    # Verificar se o setor está relacionado a um gabinete
    try:
        from apps.gabinetes.models import Gabinete
        context['gabinetes_relacionados'] = Gabinete.objects.filter(setor=setor)
    except ImportError:
        context['gabinetes_relacionados'] = []
    
    # Verificar se existem assessores relacionados ao setor
    context['assessores_relacionados'] = assessores
    
    return render(request, 'recepcao/confirmar_exclusao_setor.html', context)

@login_required(login_url='autenticacao:login_sistema')
@admin_required
def excluir_visitante(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    
    # Verificar se o visitante tem visitas registradas
    visitas_existentes = Visita.objects.filter(visitante=visitante).exists()
    
    if request.method == 'POST':
        if visitas_existentes:
            messages.error(request, 'Não é possível excluir um visitante com histórico de visitas.')
            return redirect('recepcao:detalhes_visitante', pk=pk)
        
        try:
            visitante.delete()
            messages.success(request, 'Visitante excluído com sucesso!')
            return redirect('recepcao:lista_visitantes')
        except Exception as e:
            messages.error(request, f'Erro ao excluir visitante: {str(e)}')
            return redirect('recepcao:detalhes_visitante', pk=pk)
    
    context = get_base_context('Excluir Visitante')
    context.update({
        'visitante': visitante,
        'visitas_existentes': visitas_existentes
    })
    return render(request, 'recepcao/confirmar_exclusao_visitante.html', context)

@login_required(login_url='autenticacao:login_sistema')
def gerar_etiqueta(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    context = get_base_context('Etiqueta da Visita')
    context.update({
        'visita': visita,
        'nome_exibicao': visita.visitante.nome_social if visita.visitante.nome_social else visita.visitante.nome_completo
    })
    return render(request, 'recepcao/etiqueta_visita.html', context)

@login_required(login_url='autenticacao:login_sistema')
def alterar_horario_departamento(request):
    # Verificar se o usuário é um assessor
    try:
        assessor = Assessor.objects.get(nome_responsavel=request.user.get_full_name())
    except Assessor.DoesNotExist:
        messages.error(request, 'Você não tem permissão para alterar horários de departamentos.')
        return redirect('recepcao:home_recepcao')
    
    # Obter o departamento do assessor
    departamento = assessor.departamento
    
    if request.method == 'POST':
        form = AlterarHorarioSetorForm(request.POST, instance=departamento, assessor=assessor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário do departamento alterado com sucesso!')
            return redirect('recepcao:home_recepcao')
    else:
        form = AlterarHorarioSetorForm(instance=departamento, assessor=assessor)
    
    context = get_base_context('Alterar Horário do Departamento')
    context.update({
        'form': form,
        'departamento': departamento
    })
    
    return render(request, 'recepcao/alterar_horario_departamento.html', context)

@login_required
def home_gabinetes(request):
    """View para a página inicial dos gabinetes."""
    # Se for assessor, mostra só o gabinete dele
    if hasattr(request.user, 'assessor') and request.user.assessor.departamento and request.user.assessor.departamento.tipo == 'gabinete':
        gabinetes = Setor.objects.filter(id=request.user.assessor.departamento.id, tipo='gabinete')
    else:
        gabinetes = Setor.objects.filter(tipo='gabinete')

    # Calcula estatísticas
    total_visitas = Visita.objects.count()
    visitas_hoje = Visita.objects.filter(
        data_entrada__date=timezone.now().date()
    ).count()
    visitas_em_andamento = Visita.objects.filter(
        data_saida__isnull=True
    ).count()
    hoje = timezone.now()
    primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    visitas_mes = Visita.objects.filter(
        data_entrada__gte=primeiro_dia_mes
    ).count()

    context = {
        'gabinetes': gabinetes,
        'total_visitas': total_visitas,
        'visitas_hoje': visitas_hoje,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_mes': visitas_mes,
    }
    return render(request, 'recepcao/home_gabinetes.html', context)

@login_required
def detalhes_gabinete(request, gabinete_id):
    gabinete = get_object_or_404(Setor, id=gabinete_id, tipo='gabinete')
    
    # Obter filtros da requisição
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
    objetivo = request.GET.get('objetivo')
    formato = request.GET.get('formato')
    
    # Query base
    visitas = Visita.objects.filter(setor=gabinete)
    
    # Aplicar filtros
    if data_inicio and data_fim:
        visitas = visitas.filter(
            data_entrada__date__range=[data_inicio, data_fim]
        )
    if status:
        visitas = visitas.filter(status=status)
    if objetivo:
        visitas = visitas.filter(objetivo=objetivo)
    
    # Ordenar por data de entrada (mais recentes primeiro)
    visitas = visitas.order_by('-data_entrada')
    
    # Verificar se é uma requisição de exportação
    if formato in ['pdf', 'excel']:
        if formato == 'pdf':
            return gerar_pdf_visitas(visitas, gabinete)
        else:
            return gerar_excel_visitas(visitas, gabinete)
    
    # Paginação
    paginator = Paginator(visitas, 10)  # 10 itens por página
    page = request.GET.get('page')
    visitas_paginadas = paginator.get_page(page)
    
    # Estatísticas
    visitas_hoje = visitas.filter(data_entrada__date=timezone.now().date()).count()
    visitas_em_andamento = visitas.filter(status='em_andamento').count()
    total_visitas = visitas.count()
    visitas_mes = visitas.filter(data_entrada__month=timezone.now().month).count()
    
    context = get_base_context(f'Detalhes do Gabinete - {gabinete.nome_vereador}')
    context.update({
        'gabinete': gabinete,
        'visitas': visitas_paginadas,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'status': status,
            'objetivo': objetivo
        },
        'visitas_hoje': visitas_hoje,
        'visitas_em_andamento': visitas_em_andamento,
        'total_visitas': total_visitas,
        'visitas_mes': visitas_mes,
        'TIPOS_VISITA': Visita.OBJETIVO_CHOICES
    })
    
    return render(request, 'recepcao/detalhes_gabinete.html', context)

@login_required(login_url='autenticacao:login_sistema')
def editar_gabinete(request, gabinete_id):
    gabinete = get_object_or_404(Setor, id=gabinete_id, tipo='gabinete')
    # Só o assessor responsável pode editar
    if not hasattr(request.user, 'assessor') or request.user.assessor.departamento_id != gabinete.id:
        raise PermissionDenied('Você não tem permissão para editar este gabinete.')

    if request.method == 'POST':
        form = SetorForm(request.POST, instance=gabinete, hide_responsavel=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações do gabinete atualizadas com sucesso!')
            return redirect('recepcao:detalhes_gabinete', gabinete_id=gabinete.id)
    else:
        form = SetorForm(instance=gabinete, hide_responsavel=True)

    context = get_base_context('Editar Gabinete')
    context.update({
        'form': form,
        'gabinete': gabinete,
        'is_editing': True
    })
    return render(request, 'recepcao/editar_gabinete.html', context)

def gerar_pdf_visitas(visitas, gabinete):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="visitas_{gabinete.nome_vereador}_{timezone.now().strftime("%Y%m%d")}.pdf"'
    
    # Criar o PDF
    p = canvas.Canvas(response)
    
    # Configurações iniciais
    p.setTitle(f"Relatório de Visitas - {gabinete.nome_vereador}")
    p.setFont("Helvetica-Bold", 16)
    
    # Título
    p.drawString(50, 800, f"Relatório de Visitas - {gabinete.nome_vereador}")
    p.setFont("Helvetica", 12)
    p.drawString(50, 780, f"Gerado em: {timezone.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Cabeçalho da tabela
    p.setFont("Helvetica-Bold", 10)
    headers = ["Visitante", "Data/Hora Entrada", "Data/Hora Saída", "Status", "Tipo"]
    col_widths = [150, 100, 100, 80, 100]  # Ajustado para melhor distribuição
    col_positions = [50, 200, 300, 400, 480]  # Posições ajustadas das colunas
    y = 750
    
    # Desenhar cabeçalhos
    for i, header in enumerate(headers):
        p.drawString(col_positions[i], y, header)
    
    # Dados da tabela
    p.setFont("Helvetica", 9)  # Fonte um pouco menor para melhor ajuste
    y -= 20
    
    for visita in visitas:
        if y < 50:  # Nova página se necessário
            p.showPage()
            y = 750
            # Redesenhar cabeçalho
            p.setFont("Helvetica-Bold", 10)
            for i, header in enumerate(headers):
                p.drawString(col_positions[i], y, header)
            p.setFont("Helvetica", 9)
            y -= 20
        
        # Visitante
        p.drawString(col_positions[0], y, visita.visitante.nome_completo[:30] + "..." if len(visita.visitante.nome_completo) > 30 else visita.visitante.nome_completo)
        
        # Data/Hora Entrada
        p.drawString(col_positions[1], y, visita.data_entrada.strftime("%d/%m/%Y %H:%M"))
        
        # Data/Hora Saída
        p.drawString(col_positions[2], y, visita.data_saida.strftime("%d/%m/%Y %H:%M") if visita.data_saida else "-")
        
        # Status
        p.drawString(col_positions[3], y, visita.get_status_display())
        
        # Tipo
        p.drawString(col_positions[4], y, visita.get_objetivo_display())
        
        y -= 20
    
    p.save()
    return response

def gerar_excel_visitas(visitas, gabinete):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="visitas_{gabinete.nome_vereador}_{timezone.now().strftime("%Y%m%d")}.xlsx"'
    
    # Criar o arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Visitas"
    
    # Cabeçalho
    headers = ["Visitante", "Data/Hora Entrada", "Data/Hora Saída", "Status", "Tipo"]
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)
    
    # Dados
    for row, visita in enumerate(visitas, 2):
        ws.cell(row=row, column=1, value=visita.visitante.nome_completo)
        ws.cell(row=row, column=2, value=visita.data_entrada.strftime("%d/%m/%Y %H:%M"))
        ws.cell(row=row, column=3, value=visita.data_saida.strftime("%d/%m/%Y %H:%M") if visita.data_saida else "-")
        ws.cell(row=row, column=4, value=visita.get_status_display())
        ws.cell(row=row, column=5, value=visita.get_objetivo_display())
    
    # Ajustar largura das colunas
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 20
    
    wb.save(response)
    return response

def exportar_relatorio(visitas, formato):
    if formato == 'pdf':
        return gerar_pdf(visitas)
    else:
        return gerar_excel(visitas)

def gerar_pdf(visitas):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Relatório de Visitas")
    
    # Tabela
    y = 700
    p.setFont("Helvetica", 10)
    for visita in visitas:
        p.drawString(50, y, f"Visitante: {visita.visitante.nome_completo}")
        p.drawString(50, y-20, f"Data Entrada: {visita.data_entrada.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(50, y-40, f"Status: {visita.get_status_display()}")
        y -= 60
        
        if y < 50:
            p.showPage()
            y = 750
    
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def gerar_excel(visitas):
    from openpyxl import Workbook
    from io import BytesIO
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Visitas"
    
    # Cabeçalhos
    ws.append(['Visitante', 'Data Entrada', 'Data Saída', 'Status', 'Tipo'])
    
    # Dados
    for visita in visitas:
        ws.append([
            visita.visitante.nome_completo,
            visita.data_entrada.strftime('%d/%m/%Y %H:%M'),
            visita.data_saida.strftime('%d/%m/%Y %H:%M') if visita.data_saida else '-',
            visita.get_status_display(),
            visita.get_tipo_visita_display()
        ])
    
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@login_required(login_url='autenticacao:login_sistema')
def home_departamentos(request):
    departamentos = Setor.objects.filter(tipo='departamento')
    context = {
        'departamentos': departamentos,
    }
    return render(request, 'recepcao/home_departamentos.html', context)

@login_required(login_url='autenticacao:login_sistema')
def detalhes_departamento(request, departamento_id):
    departamento = get_object_or_404(Setor, id=departamento_id, tipo='departamento')
    visitas = Visita.objects.filter(setor=departamento).order_by('-data_entrada')
    context = {
        'departamento': departamento,
        'visitas': visitas,
    }
    return render(request, 'recepcao/detalhes_departamento.html', context)

@login_required(login_url='autenticacao:login_sistema')
def visitas_tabela_departamento(request, departamento_id):
    departamento = get_object_or_404(Setor, id=departamento_id, tipo='departamento')
    visitas = Visita.objects.filter(setor=departamento).order_by('-data_entrada')
    # Filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
    objetivo = request.GET.get('objetivo')
    if data_inicio:
        visitas = visitas.filter(data_entrada__date__gte=data_inicio)
    if data_fim:
        visitas = visitas.filter(data_entrada__date__lte=data_fim)
    if status:
        visitas = visitas.filter(status=status)
    if objetivo:
        visitas = visitas.filter(objetivo=objetivo)
    html = render_to_string('recepcao/includes/tabela_visitas_departamento.html', {'visitas': visitas})
    return JsonResponse({'html': html})

@login_required(login_url='autenticacao:login_sistema')
def visitas_tabela_gabinete(request, gabinete_id):
    gabinete = get_object_or_404(Setor, id=gabinete_id, tipo='gabinete')
    visitas = Visita.objects.filter(setor=gabinete).order_by('-data_entrada')
    # Filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
    objetivo = request.GET.get('objetivo')
    if data_inicio:
        visitas = visitas.filter(data_entrada__date__gte=data_inicio)
    if data_fim:
        visitas = visitas.filter(data_entrada__date__lte=data_fim)
    if status:
        visitas = visitas.filter(status=status)
    if objetivo:
        visitas = visitas.filter(objetivo=objetivo)
    html = render_to_string('recepcao/includes/tabela_visitas_gabinete.html', {'visitas': visitas})
    return JsonResponse({'html': html})

@login_required(login_url='autenticacao:login_sistema')
def upload_foto_visitante(request, visitante_id):
    """View para gerenciar o upload de fotos dos visitantes"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        visitante = Visitante.objects.get(id=visitante_id)
    except Visitante.DoesNotExist:
        logger.error(f'Visitante {visitante_id} não encontrado')
        return JsonResponse({'success': False, 'message': 'Visitante não encontrado.'})
    
    if request.method == 'POST':
        logger.info(f'Recebido POST para upload de foto do visitante {visitante_id}')
        logger.info(f'Files no request: {request.FILES}')
        
        if 'foto' in request.FILES:
            logger.info('Foto encontrada no request')
            try:
                # Remove foto antiga se existir
                if visitante.foto:
                    visitante.foto.delete()
                # Salva nova foto
                visitante.foto = request.FILES['foto']
                visitante.save()
                logger.info('Foto salva com sucesso')

                return JsonResponse({
                    'success': True, 
                    'message': 'Foto enviada com sucesso!',
                    'redirect_url': reverse('recepcao:detalhes_visitante', args=[visitante_id])
                })
            except Exception as e:
                logger.error(f'Erro ao salvar foto: {str(e)}')
                return JsonResponse({'success': False, 'message': f'Erro ao salvar foto: {str(e)}'})
        else:
            logger.error('Nenhuma foto encontrada no request')
            return JsonResponse({'success': False, 'message': 'Nenhuma foto foi enviada.'})
    
    return render(request, 'recepcao/upload_foto.html', {'visitante': visitante})

@login_required
@staff_member_required
def get_assessores_por_tipo(request):
    """
    Retorna uma lista de assessores filtrados por tipo de setor.
    """
    tipo = request.GET.get('tipo')
    assessores = Assessor.objects.filter(
        ativo=True,
        departamento__tipo=tipo
    ).order_by('nome_responsavel')
    
    data = [
        {
            'id': assessor.id,
            'text': f"{assessor.nome_responsavel} ({assessor.get_funcao_display()})"
        }
        for assessor in assessores
    ]
    
    return JsonResponse(data, safe=False)

@login_required
@staff_member_required
def get_assessor_info(request):
    """
    Retorna as informações detalhadas de um assessor.
    """
    assessor_id = request.GET.get('assessor_id')
    try:
        assessor = Assessor.objects.get(id=assessor_id, ativo=True)
        data = {
            'email': assessor.email,
            'funcao': assessor.funcao,
            'horario_entrada': assessor.horario_entrada.strftime('%H:%M') if assessor.horario_entrada else '',
            'horario_saida': assessor.horario_saida.strftime('%H:%M') if assessor.horario_saida else ''
        }
        return JsonResponse(data)
    except Assessor.DoesNotExist:
        return JsonResponse({'error': 'Assessor não encontrado'}, status=404)

@login_required(login_url='autenticacao:login_sistema')
def status_visita_ajax(request):
    """
    Retorna apenas a tabela de visitas filtrada via AJAX.
    """
    # Usar a mesma lógica da view principal
    data = request.GET.get('data')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    localizacao = request.GET.get('localizacao')
    setor = request.GET.get('setor')

    # Iniciar queryset com visitas não finalizadas e status em andamento
    visitas = Visita.objects.filter(
        data_saida__isnull=True,
        status='em_andamento'
    )

    # Aplicar filtros
    if data:
        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
            visitas = visitas.filter(data_entrada__date=data)
        except (ValueError, TypeError):
            pass

    if hora_inicio:
        try:
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            visitas = visitas.filter(data_entrada__time__gte=hora_inicio)
        except (ValueError, TypeError):
            pass

    if hora_fim:
        try:
            hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
            visitas = visitas.filter(data_entrada__time__lte=hora_fim)
        except (ValueError, TypeError):
            pass

    if localizacao:
        visitas = visitas.filter(localizacao=localizacao)

    if setor:
        visitas = visitas.filter(setor_id=setor)

    # Ordenar por data de entrada mais recente
    visitas = visitas.order_by('-data_entrada')

    # Renderizar apenas a tabela
    table_html = render_to_string(
        'recepcao/includes/tabela_visitas_status.html',
        {'visitas': visitas},
        request=request
    )

    return JsonResponse({
        'success': True,
        'html': table_html,
        'total_visitas': visitas.count()
    })

@login_required(login_url='autenticacao:login_sistema')
def historico_visitas_ajax(request):
    """
    Retorna apenas a tabela do histórico de visitas filtrada via AJAX.
    """
    # Usar a mesma lógica da view principal
    status = request.GET.get('status')
    periodo = request.GET.get('periodo')
    busca = request.GET.get('busca')
    
    # Query base
    visitas = Visita.objects.all()
    
    # Aplicar filtros
    if status:
        if status == 'em_andamento':
            visitas = visitas.filter(data_saida__isnull=True)
        elif status == 'finalizada':
            visitas = visitas.filter(data_saida__isnull=False)
    
    if periodo:
        hoje = timezone.localtime().date()
        if periodo == 'hoje':
            visitas = visitas.filter(data_entrada__date=hoje)
        elif periodo == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            visitas = visitas.filter(data_entrada__date__gte=inicio_semana)
        elif periodo == 'mes':
            inicio_mes = hoje.replace(day=1)
            visitas = visitas.filter(data_entrada__date__gte=inicio_mes)
    
    if busca:
        visitas = visitas.filter(
            Q(visitante__nome_completo__icontains=busca) |
            Q(visitante__CPF__icontains=busca)
        )
    
    # Ordenação
    visitas = visitas.order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(visitas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_visitas = visitas.count()
    visitas_em_andamento = visitas.filter(data_saida__isnull=True).count()
    visitas_finalizadas = visitas.filter(data_saida__isnull=False).count()

    # Renderizar apenas a tabela e estatísticas
    table_html = render_to_string(
        'recepcao/includes/tabela_historico_visitas.html',
        {
            'page_obj': page_obj,
            'status_filtro': status,
            'periodo_filtro': periodo,
            'busca': busca,
        },
        request=request
    )
    
    stats_html = render_to_string(
        'recepcao/includes/stats_historico_visitas.html',
        {
            'total_visitas': total_visitas,
            'visitas_em_andamento': visitas_em_andamento,
            'visitas_finalizadas': visitas_finalizadas,
        },
        request=request
    )

    return JsonResponse({
        'success': True,
        'html': table_html,
        'stats_html': stats_html,
        'total_visitas': total_visitas,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas': visitas_finalizadas,
    })