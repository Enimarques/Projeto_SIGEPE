from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Veiculo

@login_required(login_url='autenticacao:login_sistema')
def home_veiculos(request):
    hoje = datetime.now().date()
    
    # Veículos no estacionamento
    veiculos_presentes = Veiculo.objects.filter(
        data_entrada__isnull=False,
        data_saida__isnull=True
    ).count()
    
    # Total de veículos registrados hoje
    veiculos_hoje = Veiculo.objects.filter(
        data_entrada__date=hoje
    ).count()
    
    # Total de veículos registrados no mês
    veiculos_mes = Veiculo.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month
    ).count()
    
    context = {
        'veiculos_presentes': veiculos_presentes,
        'veiculos_hoje': veiculos_hoje,
        'veiculos_mes': veiculos_mes,
    }
    
    return render(request, 'veiculos/home_veiculos.html', context)

@login_required(login_url='autenticacao:login_sistema')
def lista_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-data_entrada')
    return render(request, 'veiculos/lista_veiculos.html', {'veiculos': veiculos})

@login_required(login_url='autenticacao:login_sistema')
def registro_entrada(request):
    if request.method == 'POST':
        # Lógica para registrar entrada
        pass
    return render(request, 'veiculos/registro_entrada.html')

@login_required(login_url='autenticacao:login_sistema')
def registro_saida(request):
    veiculos = Veiculo.objects.filter(data_saida__isnull=True)
    return render(request, 'veiculos/registro_saida.html', {'veiculos': veiculos})

@login_required(login_url='autenticacao:login_sistema')
def registrar_saida(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    if request.method == 'POST':
        veiculo.data_saida = datetime.now()
        veiculo.save()
        messages.success(request, 'Saída registrada com sucesso!')
        return redirect('veiculos:lista_veiculos')
    return render(request, 'veiculos/registrar_saida.html', {'veiculo': veiculo})
