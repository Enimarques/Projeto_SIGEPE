from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Visitante, Visita
from apps.veiculos.models import Veiculo
from .forms import VisitanteForm, VisitaForm
from django.utils import timezone
from datetime import datetime, timedelta

@login_required(login_url='autenticacao:login_sistema')
def home_sistema(request):
    hoje = timezone.now().date()
    
    # Visitas hoje
    visitas_hoje = Visita.objects.filter(
        data_entrada__date=hoje
    ).count()
    
    # Visitas em andamento
    visitas_em_andamento = Visita.objects.filter(
        status='em_andamento'
    ).count()
    
    # Total de visitantes cadastrados
    total_visitantes = Visitante.objects.count()
    
    # Veículos presentes no estacionamento
    veiculos_presentes = Veiculo.objects.filter(
        horario_entrada__isnull=False,
        horario_saida__isnull=True,
        status='presente'
    ).count()
    
    context = {
        'visitas_hoje': visitas_hoje,
        'visitas_em_andamento': visitas_em_andamento,
        'total_visitantes': total_visitantes,
        'veiculos_presentes': veiculos_presentes,
        'title': 'Dashboard - URUTAU'
    }
    
    return render(request, 'main/recepcao/home_sistema.html', context)

@login_required(login_url='autenticacao:login_sistema')
def status_visita(request):
    visitas_em_andamento = Visita.objects.filter(status='em_andamento').order_by('-data_entrada')
    context = {
        'visitas_em_andamento': visitas_em_andamento,
        'total_em_andamento': visitas_em_andamento.count(),
    }
    return render(request, 'main/recepcao/status_visita.html', context)

@login_required(login_url='autenticacao:login_sistema')
def cadastro_visitantes(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST, request.FILES)
        if form.is_valid():
            visitante = form.save()
            messages.success(request, 'Visitante cadastrado com sucesso!')
            return redirect('main:lista_visitantes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = VisitanteForm()
    
    return render(request, 'main/visitantes/cadastro_visitantes.html', {'form': form})

@login_required(login_url='autenticacao:login_sistema')
def lista_visitantes(request):
    visitantes = Visitante.objects.all().order_by('nome_completo')
    return render(request, 'main/visitantes/lista_visitantes.html', {'visitantes': visitantes})

@login_required(login_url='autenticacao:login_sistema')
def registro_visitas(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.data_entrada = timezone.now()
            visita.status = 'em_andamento'
            visita.save()
            messages.success(request, f'Visita de {visita.visitante.nome_completo} registrada com sucesso!')
            return redirect('main:status_visita')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = VisitaForm()
    
    return render(request, 'main/visitantes/registro_visitas.html', {'form': form})

@login_required(login_url='autenticacao:login_sistema')
def historico_visitas(request):
    visitas = Visita.objects.all().order_by('-data_entrada')
    visitas_em_andamento = visitas.filter(status='em_andamento')
    visitas_finalizadas = visitas.filter(status='finalizada')
    
    context = {
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas': visitas_finalizadas,
        'total_em_andamento': visitas_em_andamento.count(),
        'total_finalizadas': visitas_finalizadas.count(),
    }
    return render(request, 'main/visitantes/historico_visitas.html', context)

@login_required(login_url='autenticacao:login_sistema')
def finalizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    if visita.status == 'em_andamento':
        visita.registrar_saida()
        messages.success(request, f'Visita de {visita.visitante.nome_completo} finalizada com sucesso!')
    else:
        messages.warning(request, 'Esta visita já foi finalizada.')
    return redirect('main:status_visita')