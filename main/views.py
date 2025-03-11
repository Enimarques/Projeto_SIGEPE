from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Visitante, Visita, Setor
from .forms import RegisterForm, VisitaForm, FimVisitaForm
from django.utils import timezone

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
def cadastrar_visitante(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            visitante = form.save()
            messages.success(request, 'Visitante cadastrado com sucesso!')
            return redirect('main:lista_visitantes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = RegisterForm()
    
    return render(request, 'main/cadastrar_visitante.html', {'form': form})

@login_required
def lista_visitantes(request):
    visitantes = Visitante.objects.all().order_by('nome_completo')
    return render(request, 'main/lista_visitantes.html', {'visitantes': visitantes})

@login_required
def cadastrar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.data_visita = timezone.now()
            visita.save()
            messages.success(request, f'Visita de {visita.nome_visitante} registrada com sucesso!')
            return redirect('main:lista_visitas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = VisitaForm()
    
    return render(request, 'main/cadastrar_visita.html', {'form': form})

@login_required
def lista_visitas(request):
    visitas = Visita.objects.all().order_by('-data_visita')
    visitas_em_andamento = visitas.filter(horario_saida__isnull=True)
    visitas_finalizadas = visitas.filter(horario_saida__isnull=False)
    
    context = {
        'visitas_em_andamento': visitas_em_andamento,
        'visitas_finalizadas': visitas_finalizadas,
        'total_em_andamento': visitas_em_andamento.count(),
        'total_finalizadas': visitas_finalizadas.count(),
    }
    return render(request, 'main/lista_visitas.html', context)

@login_required
def registrar_saida(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    if not visita.horario_saida:
        visita.registrar_saida()
        messages.success(request, f'Saída de {visita.nome_visitante} registrada com sucesso!')
    else:
        messages.warning(request, 'Esta visita já possui registro de saída.')
    return redirect('main:lista_visitas')

@login_required
def recepcao(request):
    visitas_em_andamento = Visita.objects.filter(horario_saida__isnull=True).order_by('-data_visita')
    context = {
        'visitas_em_andamento': visitas_em_andamento,
        'total_em_andamento': visitas_em_andamento.count(),
    }
    return render(request, 'main/recepcao.html', context)