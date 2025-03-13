from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Veiculo
from .forms import VeiculoForm, SaidaVeiculoForm

@login_required(login_url='autenticacao:login_sistema')
def lista_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-horario_entrada')
    veiculos_em_patio = veiculos.filter(horario_saida__isnull=True)
    veiculos_saida = veiculos.filter(horario_saida__isnull=False)
    
    context = {
        'veiculos_em_patio': veiculos_em_patio,
        'veiculos_saida': veiculos_saida,
        'total_em_patio': veiculos_em_patio.count(),
        'total_saida': veiculos_saida.count(),
    }
    return render(request, 'veiculos/lista_veiculos.html', context)

@login_required(login_url='autenticacao:login_sistema')
def registro_entrada(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.horario_entrada = timezone.now()
            veiculo.save()
            messages.success(request, 'Entrada do veículo registrada com sucesso!')
            return redirect('veiculos:lista_veiculos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = VeiculoForm()
    return render(request, 'veiculos/registro_entrada.html', {'form': form})

@login_required(login_url='autenticacao:login_sistema')
def registro_saida(request):
    if request.method == 'POST':
        form = SaidaVeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.cleaned_data['placa']
            veiculo.horario_saida = timezone.now()
            veiculo.observacoes = form.cleaned_data.get('observacoes', '')
            veiculo.status = 'saida'
            veiculo.save()
            messages.success(request, 'Saída do veículo registrada com sucesso!')
            return redirect('veiculos:lista_veiculos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SaidaVeiculoForm()
    return render(request, 'veiculos/registro_saida.html', {'form': form})

@login_required(login_url='autenticacao:login_sistema')
def detalhes_veiculo(request, placa):
    veiculo = get_object_or_404(Veiculo, placa=placa)
    return render(request, 'veiculos/detalhes_veiculo.html', {'veiculo': veiculo})
