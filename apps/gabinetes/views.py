from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
from apps.recepcao.models import Visita, Setor, Assessor
from apps.autenticacao.decorators import assessor_gabinete_access, block_assessor
import json

@login_required(login_url='autenticacao:login_sistema')
def finalizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    gabinete_id = visita.setor.id
    
    if not visita.data_saida:
        visita.data_saida = timezone.now()
        visita.status = 'finalizada'
        visita.save()
        messages.success(request, 'Visita finalizada com sucesso!')
    
    return redirect('gabinetes:detalhes_gabinete', pk=gabinete_id)

@login_required(login_url='autenticacao:login_sistema')
@block_assessor
def home_gabinetes(request):
    hoje = datetime.now().date()
    
    # Contagem de visitas hoje
    visitas_hoje = Visita.objects.filter(
        data_entrada__date=hoje,
        setor__tipo='gabinete_vereador'
    ).count()
    
    # Visitas em andamento
    visitas_andamento = Visita.objects.filter(
        data_entrada__isnull=False,
        data_saida__isnull=True,
        setor__tipo='gabinete_vereador'
    ).count()
    
    # Total de visitas
    total_visitas = Visita.objects.filter(
        setor__tipo='gabinete_vereador'
    ).count()
    
    # Visitas do mês atual
    visitas_mes = Visita.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month,
        setor__tipo='gabinete_vereador'
    ).count()
    
    # Dados para o gráfico (últimos 7 dias)
    labels = []
    values = []
    for i in range(6, -1, -1):
        data = hoje - timedelta(days=i)
        visitas = Visita.objects.filter(
            data_entrada__date=data,
            setor__tipo='gabinete_vereador'
        ).count()
        labels.append(data.strftime('%d/%m'))
        values.append(visitas)
    
    # Obter todos os gabinetes
    gabinetes = Setor.objects.filter(tipo='gabinete_vereador')
    
    # Verifica se há visitas
    if visitas_hoje == 0 and visitas_andamento == 0:
        mensagem = 'Não há visitas registradas para hoje.'
    else:
        mensagem = None
    
    context = {
        'visitas_hoje': visitas_hoje,
        'visitas_andamento': visitas_andamento,
        'total_visitas': total_visitas,
        'visitas_mes': visitas_mes,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
        'mensagem': mensagem,
        'gabinetes': gabinetes
    }
    
    return render(request, 'gabinetes/home_gabinetes.html', context)

@login_required(login_url='autenticacao:login_sistema')
@assessor_gabinete_access
def detalhes_gabinete(request, pk):
    hoje = datetime.now().date()
    gabinete = get_object_or_404(Setor, pk=pk, tipo='gabinete_vereador')
    
    # Obter assessores do gabinete
    assessores = Assessor.objects.filter(departamento=gabinete)
    
    # Verificar se o usuário é um assessor e se tem acesso a este gabinete
    is_assessor = False
    has_access = True  # Por padrão, usuários não assessores têm acesso completo
    
    try:
        # Verifica se o usuário é um assessor
        assessor = request.user.assessor
        is_assessor = True
        
        # Verifica se o assessor pertence a este gabinete
        if assessor.departamento.id != gabinete.id:
            # Se não pertencer, não mostra dados de visitantes e histórico
            has_access = False
    except AttributeError:
        # Se não for assessor, permite o acesso normalmente (admin ou outros usuários)
        pass
    
    # Inicializa variáveis para o contexto
    visitantes_aguardando = None
    visitas_hoje = 0
    total_visitas = 0
    historico_visitas = None
    
    # Obter visitantes aguardando atendimento
    visitantes_aguardando = Visita.objects.filter(
        setor=gabinete,
        data_entrada__isnull=False,
        data_saida__isnull=True
    ).order_by('data_entrada')
    
    # Estatísticas de visitas
    visitas_hoje = Visita.objects.filter(
        setor=gabinete,
        data_entrada__date=hoje
    ).count()
    
    total_visitas = Visita.objects.filter(setor=gabinete).count()
    
    # Histórico de visitas (com filtro de data opcional)
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    historico_query = Visita.objects.filter(setor=gabinete)
    
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        historico_query = historico_query.filter(data_entrada__date__gte=data_inicio)
    else:
        # Padrão: último mês
        data_inicio = hoje - timedelta(days=30)
        historico_query = historico_query.filter(data_entrada__date__gte=data_inicio)
    
    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        historico_query = historico_query.filter(data_entrada__date__lte=data_fim)
    else:
        data_fim = hoje
    
    historico_visitas = historico_query.order_by('-data_entrada')
    
    context = {
        'gabinete': gabinete,
        'has_access': has_access
    }
    
    if has_access:
        # Obter visitantes aguardando atendimento
        visitantes_aguardando = Visita.objects.filter(
            setor=gabinete,
            data_entrada__isnull=False,
            data_saida__isnull=True
        ).order_by('data_entrada')
        
        # Estatísticas de visitas
        visitas_hoje = Visita.objects.filter(
            setor=gabinete,
            data_entrada__date=hoje
        ).count()
        
        total_visitas = Visita.objects.filter(setor=gabinete).count()
        
        # Histórico de visitas (com filtro de data opcional)
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        historico_query = Visita.objects.filter(setor=gabinete)
        
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            historico_query = historico_query.filter(data_entrada__date__gte=data_inicio)
        else:
            # Padrão: último mês
            data_inicio = hoje - timedelta(days=30)
            historico_query = historico_query.filter(data_entrada__date__gte=data_inicio)
        
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            historico_query = historico_query.filter(data_entrada__date__lte=data_fim)
        else:
            data_fim = hoje
        
        historico_visitas = historico_query.order_by('-data_entrada')
    else:
        # Se não tiver acesso, define valores padrão para as datas
        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje
    
    context = {
        'gabinete': gabinete,
        'assessores': assessores,
        'visitantes_aguardando': visitantes_aguardando,
        'visitas_hoje': visitas_hoje,
        'total_visitas': total_visitas,
        'historico_visitas': historico_visitas,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'is_assessor': is_assessor,
        'has_access': has_access
    }
    
    return render(request, 'gabinetes/detalhes_gabinete.html', context)
