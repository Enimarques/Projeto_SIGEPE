from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from apps.recepcao.models import Visita
import json

@login_required(login_url='autenticacao:login_sistema')
def home_gabinetes(request):
    hoje = datetime.now().date()
    
    # Contagem de visitas hoje
    visitas_hoje = Visita.objects.filter(
        data_entrada__date=hoje,
        setor='gabinete_vereador'
    ).count()
    
    # Visitas em andamento
    visitas_andamento = Visita.objects.filter(
        data_entrada__isnull=False,
        data_saida__isnull=True,
        setor='gabinete_vereador'
    ).count()
    
    # Total de visitas
    total_visitas = Visita.objects.filter(
        setor='gabinete_vereador'
    ).count()
    
    # Visitas do mês atual
    visitas_mes = Visita.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month,
        setor='gabinete_vereador'
    ).count()
    
    # Dados para o gráfico (últimos 7 dias)
    labels = []
    values = []
    for i in range(6, -1, -1):
        data = hoje - timedelta(days=i)
        visitas = Visita.objects.filter(
            data_entrada__date=data,
            setor='gabinete_vereador'
        ).count()
        labels.append(data.strftime('%d/%m'))
        values.append(visitas)
    
    # Verifica se há visitas
    if visitas_hoje == 0 and visitas_andamento == 0:
        mensagem = 'Não há visitas registradas para hoje.'
    else:
        mensagem = None

    context = {
        'title': 'Gabinetes - URUTAU',
        'visitas_hoje': visitas_hoje,
        'visitas_andamento': visitas_andamento,
        'total_visitas': total_visitas,
        'visitas_mes': visitas_mes,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
        'mensagem': mensagem,
    }
    
    return render(request, 'gabinetes/home_gabinetes.html', context)
