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
        setor_destino__tipo='gabinete'
    ).count()
    
    # Visitas em andamento
    visitas_andamento = Visita.objects.filter(
        data_entrada__isnull=False,
        data_saida__isnull=True,
        setor_destino__tipo='gabinete'
    ).count()
    
    # Total de visitas
    total_visitas = Visita.objects.filter(
        setor_destino__tipo='gabinete'
    ).count()
    
    # Visitas do mês atual
    visitas_mes = Visita.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month,
        setor_destino__tipo='gabinete'
    ).count()
    
    # Dados para o gráfico (últimos 7 dias)
    labels = []
    values = []
    for i in range(6, -1, -1):
        data = hoje - timedelta(days=i)
        visitas = Visita.objects.filter(
            data_entrada__date=data,
            setor_destino__tipo='gabinete'
        ).count()
        labels.append(data.strftime('%d/%m'))
        values.append(visitas)
    
    context = {
        'title': 'Gabinetes - URUTAU',
        'visitas_hoje': visitas_hoje,
        'visitas_andamento': visitas_andamento,
        'total_visitas': total_visitas,
        'visitas_mes': visitas_mes,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
    }
    
    return render(request, 'gabinetes/home_gabinetes.html', context)
