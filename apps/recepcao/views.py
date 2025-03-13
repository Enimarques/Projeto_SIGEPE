from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Visitante, Visita
from .forms import VisitanteForm

@login_required(login_url='autenticacao:login_sistema')
def home_sistema(request):
    return render(request, 'main/recepcao/home_sistema.html')

@login_required(login_url='autenticacao:login_sistema')
def home_recepcao(request):
    hoje = timezone.localtime().date()
    
    # Contagem de visitas
    visitas_hoje = Visita.objects.filter(data_entrada__date=hoje).count()
    visitas_andamento = Visita.objects.filter(data_saida__isnull=True).count()
    total_visitantes = Visitante.objects.count()
    
    return render(request, 'recepcao/home_recepcao.html', {
        'title': 'Recepção - URUTAU',
        'visitas_hoje': visitas_hoje,
        'visitas_andamento': visitas_andamento,
        'total_visitantes': total_visitantes,
    })

@login_required(login_url='autenticacao:login_sistema')
def lista_visitantes(request):
    visitantes = Visitante.objects.all().order_by('-data_cadastro')
    return render(request, 'recepcao/lista_visitantes.html', {
        'title': 'Lista de Visitantes - URUTAU',
        'visitantes': visitantes
    })

@login_required(login_url='autenticacao:login_sistema')
def cadastro_visitantes(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST, request.FILES)
        if form.is_valid():
            visitante = form.save()
            messages.success(request, 'Visitante cadastrado com sucesso!')
            return redirect('recepcao:detalhes_visitante', pk=visitante.pk)
    else:
        form = VisitanteForm()

    context = {
        'title': 'Cadastro de Visitantes - URUTAU',
        'form': form,
        'estados': dict(Visitante.ESTADOS_CHOICES)
    }
    return render(request, 'recepcao/cadastro_visitantes.html', context)

@login_required(login_url='autenticacao:login_sistema')
def detalhes_visitante(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    return render(request, 'recepcao/detalhes_visitante.html', {
        'title': f'Detalhes do Visitante {visitante.nome_completo} - URUTAU',
        'visitante': visitante
    })

@login_required(login_url='autenticacao:login_sistema')
def registro_visitas(request):
    return render(request, 'recepcao/registro_visitas.html', {
        'title': 'Registro de Visitas - URUTAU'
    })

@login_required(login_url='autenticacao:login_sistema')
def historico_visitas(request):
    # Filtros
    status = request.GET.get('status')
    periodo = request.GET.get('periodo')
    busca = request.GET.get('busca')
    
    # Query base
    visitas = Visita.objects.all()
    
    # Aplicar filtros
    if status:
        visitas = visitas.filter(status=status)
    
    if periodo:
        hoje = timezone.localtime().date()
        if periodo == 'hoje':
            visitas = visitas.filter(data_entrada__date=hoje)
        elif periodo == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            visitas = visitas.filter(data_entrada__date__gte=inicio_semana)
        elif periodo == 'mes':
            visitas = visitas.filter(data_entrada__month=hoje.month)
    
    if busca:
        visitas = visitas.filter(visitante__nome_completo__icontains=busca)
    
    # Ordenação
    visitas = visitas.order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(visitas, 10)  # 10 visitas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_visitas = visitas.count()
    visitas_em_andamento = visitas.filter(status='em_andamento').count()
    visitas_finalizadas = visitas.filter(status='finalizada').count()
    visitas_canceladas = visitas.filter(status='cancelada').count()
    
    context = {
        'title': 'Histórico de Visitas - URUTAU',
        'page_obj': page_obj,
        'total_visitas': total_visitas,
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas': visitas_finalizadas,
        'visitas_canceladas': visitas_canceladas,
        # Manter filtros selecionados
        'status_filtro': status,
        'periodo_filtro': periodo,
        'busca': busca,
    }
    
    return render(request, 'recepcao/historico_visitas.html', context)

@login_required(login_url='autenticacao:login_sistema')
def status_visita(request):
    # Query base: visitas em andamento
    visitas = Visita.objects.filter(status='em_andamento')
    
    # Filtros
    data = request.GET.get('data')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    localizacao = request.GET.get('localizacao')
    setor = request.GET.get('setor')
    
    # Aplicar filtros
    if data:
        visitas = visitas.filter(data_entrada__date=datetime.strptime(data, '%Y-%m-%d').date())
    
    if hora_inicio:
        visitas = visitas.filter(data_entrada__time__gte=datetime.strptime(hora_inicio, '%H:%M').time())
    
    if hora_fim:
        visitas = visitas.filter(data_entrada__time__lte=datetime.strptime(hora_fim, '%H:%M').time())
    
    if localizacao:
        visitas = visitas.filter(localizacao=localizacao)
    
    if setor:
        visitas = visitas.filter(setor=setor)
    
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
    
    context = {
        'title': 'Status das Visitas - URUTAU',
        'visitas': visitas,
        'total_em_andamento': total_em_andamento,
        'total_por_local': total_por_local,
        'setores': dict(Visita.SETOR_CHOICES),
        'localizacoes': dict(Visita.LOCALIZACAO_CHOICES),
        # Manter filtros selecionados
        'data_filtro': data,
        'hora_inicio_filtro': hora_inicio,
        'hora_fim_filtro': hora_fim,
        'localizacao_filtro': localizacao,
        'setor_filtro': setor
    }
    
    return render(request, 'recepcao/status_visita.html', context)

@login_required(login_url='autenticacao:login_sistema')
def finalizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    if not visita.data_saida:
        visita.data_saida = timezone.now()
        visita.save()
    return redirect('recepcao:status_visita')