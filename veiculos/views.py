from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Veiculo
from .forms import VeiculoForm, SaidaVeiculoForm

def lista_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-horario_entrada')
    return render(request, 'veiculos/lista_veiculos.html', {'veiculos': veiculos})

def entrada_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.horario_entrada = timezone.now()
            veiculo.save()
            messages.success(request, 'Veículo registrado com sucesso!')
            return redirect('lista_veiculos')
    else:
        form = VeiculoForm()
    return render(request, 'veiculos/entrada_veiculo.html', {'form': form})

def saida_veiculo(request):
    if request.method == 'POST':
        form = SaidaVeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.cleaned_data['placa']
            veiculo.horario_saida = form.cleaned_data['horario_saida']
            veiculo.observacoes = form.cleaned_data.get('observacoes', '')
            veiculo.status = 'saida'
            veiculo.save()
            messages.success(request, 'Saída registrada com sucesso!')
            return redirect('lista_veiculos')
    else:
        form = SaidaVeiculoForm()
    return render(request, 'veiculos/saida_veiculo.html', {'form': form})

def detalhes_veiculo(request, placa):
    veiculo = get_object_or_404(Veiculo, placa=placa)
    return render(request, 'veiculos/detalhes_veiculo.html', {'veiculo': veiculo})
