from django.shortcuts import render
from apps.recepcao.models import Visita, Visitante, Assessor
from apps.veiculos.models import Veiculo
from apps.autenticacao.services.auth_service import AuthenticationService
from django.contrib.auth.models import User, Group
import psutil
from django.http import JsonResponse
import time

# Lista global para armazenar os últimos tempos de resposta
ULTIMOS_TEMPOS = []

def registrar_tempo_resposta(tempo):
    ULTIMOS_TEMPOS.append(tempo)
    if len(ULTIMOS_TEMPOS) > 100:
        ULTIMOS_TEMPOS.pop(0)

def get_tempo_resposta_medio():
    if ULTIMOS_TEMPOS:
        return round(sum(ULTIMOS_TEMPOS) / len(ULTIMOS_TEMPOS), 2)
    return 0

def home_sistema(request):
    user = request.user
    user_groups = [g.name for g in user.groups.all()]
    is_guarita = 'Agente_Guarita' in user_groups
    is_assessor = AuthenticationService.is_assessor(user)

    context = {'title': 'Home - URUTAU'}

    if is_guarita:
        # Só mostra cards de veículos
        context['veiculos_no_estacionamento'] = Veiculo.objects.filter(status='presente').count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['is_guarita'] = True
        context['is_assessor'] = False
    else:
        # Dados da Recepção
        context['visitas_em_andamento'] = Visita.objects.filter(data_saida__isnull=True).count()
        context['total_visitantes'] = Visitante.objects.count()
        # Dados de Veículos
        context['veiculos_no_estacionamento'] = Veiculo.objects.filter(status='presente').count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['is_guarita'] = False
        context['is_assessor'] = is_assessor

    return render(request, 'main/home_sistema.html', context)

def metricas_sistema(request):
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    tempo_resposta = get_tempo_resposta_medio()  # ms
    return JsonResponse({
        'cpu': cpu,
        'mem': mem,
        'resp': tempo_resposta
    })
