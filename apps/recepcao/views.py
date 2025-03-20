from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Visitante, Visita, Setor
from .forms import VisitanteForm, VisitaForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

def check_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied

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
    # Este comentário é importante para entender a lógica de contagem de visitas
    visitas_hoje = Visita.objects.filter(data_entrada__date=hoje).count()
    visitas_em_andamento = Visita.objects.filter(data_saida__isnull=True).count()  # Removido filtro de data
    visitas_finalizadas_hoje = Visita.objects.filter(data_entrada__date=hoje, data_saida__isnull=False).count()
    total_visitantes = Visitante.objects.count()
    
    context = get_base_context()
    context.update({
        'visitas_hoje': visitas_hoje,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas_hoje': visitas_finalizadas_hoje,
        'total_visitantes': total_visitantes
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
            return redirect('recepcao:lista_visitantes')
    else:
        form = VisitanteForm()
    
    context = get_base_context('Cadastro de Visitante')
    context.update({
        'form': form
    })
    
    return render(request, 'recepcao/cadastro_visitantes.html', context)

@login_required(login_url='autenticacao:login_sistema')
def detalhes_visitante(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    context = get_base_context('Detalhes do Visitante')
    context.update({
        'visitante': visitante
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
                
                # Criar a visita usando a localização do setor
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
    cpf = request.GET.get('cpf')
    if not cpf:
        return JsonResponse({'success': False, 'message': 'CPF não fornecido'})
    
    try:
        visitante = Visitante.objects.get(CPF=cpf)
        return JsonResponse({
            'success': True,
            'visitante': {
                'nome_completo': visitante.nome_completo,
                'telefone': visitante.telefone
            }
        })
    except Visitante.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Visitante não encontrado'
        })

@login_required(login_url='autenticacao:login_sistema')
def buscar_setores(request):
    tipo = request.GET.get('tipo')
    setores = Setor.objects.filter(tipo=tipo).order_by('nome').values('id', 'nome')
    return JsonResponse({'setores': list(setores)})

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
    # Obter parâmetros do filtro
    data = request.GET.get('data')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    localizacao = request.GET.get('localizacao')
    setor = request.GET.get('setor')

    # Iniciar queryset com visitas não finalizadas
    visitas = Visita.objects.filter(data_saida__isnull=True)

    # Aplicar filtros
    if data:
        data = datetime.strptime(data, '%Y-%m-%d').date()
        visitas = visitas.filter(data_entrada__date=data)

    if hora_inicio:
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
        visitas = visitas.filter(data_entrada__time__gte=hora_inicio)

    if hora_fim:
        hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
        visitas = visitas.filter(data_entrada__time__lte=hora_fim)

    if localizacao:
        visitas = visitas.filter(localizacao=localizacao)

    if setor:
        visitas = visitas.filter(setor_id=setor)

    # Ordenar por data de entrada mais recente
    visitas = visitas.order_by('-data_entrada')

    # Estatísticas
    total_em_andamento = visitas.count()
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
        'total_por_local': total_por_local,
        'setores': Setor.objects.all().order_by('nome'),
        'localizacoes': dict(Visita.LOCALIZACAO_CHOICES),
        # Manter filtros selecionados
        'data_filtro': data,
        'hora_inicio_filtro': hora_inicio,
        'hora_fim_filtro': hora_fim,
        'localizacao_filtro': localizacao,
        'setor_filtro': setor
    })

    return render(request, 'recepcao/status_visita.html', context)

@login_required(login_url='autenticacao:login_sistema')
def finalizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    if not visita.data_saida:
        visita.data_saida = timezone.now()
        visita.status = 'finalizada'
        visita.save()
        messages.success(request, 'Visita finalizada com sucesso!')
        return redirect('recepcao:historico_visitas')
    return redirect('recepcao:historico_visitas')

@login_required(login_url='autenticacao:login_sistema')
def excluir_visita(request, pk):
    check_superuser(request.user)
    visita = get_object_or_404(Visita, pk=pk)
    visita.delete()
    messages.success(request, 'Visita excluída com sucesso!')
    return redirect('recepcao:historico_visitas')

@login_required(login_url='autenticacao:login_sistema')
def excluir_setor(request, pk):
    check_superuser(request.user)
    setor = get_object_or_404(Setor, pk=pk)
    try:
        setor.delete()
        messages.success(request, 'Setor excluído com sucesso!')
    except models.ProtectedError:
        messages.error(request, 'Não é possível excluir este setor pois existem visitas vinculadas a ele.')
    return redirect('recepcao:lista_setores')

@login_required(login_url='autenticacao:login_sistema')
def gerar_etiqueta(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    context = get_base_context('Etiqueta da Visita')
    context.update({
        'visita': visita,
        'nome_exibicao': visita.visitante.nome_social if visita.visitante.nome_social else visita.visitante.nome_completo
    })
    return render(request, 'recepcao/etiqueta_visita.html', context)