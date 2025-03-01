from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Veiculo
from .forms import VeiculoForm

def listar_veiculos(request):
    veiculos = Veiculo.objects.filter(status='dentro')
    return render(request, 'veiculos/listar_veiculos.html', {'veiculos': veiculos})

def registrar_entrada(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.horario_entrada = timezone.now()
            veiculo.status = 'dentro'
            veiculo.save()
            return redirect('home')
    else:
        form = VeiculoForm()
    return render(request, 'veiculos/entrada_veiculo.html', {'form': form})

def registrar_saida(request, veiculo_id):
    veiculo = Veiculo.objects.get(id=veiculo_id)
    if request.method == 'POST':
        veiculo.horario_saida = timezone.now()
        veiculo.status = 'fora'
        veiculo.save()
        return redirect('home')
    return render(request, 'veiculos/saida_veiculo.html', {'veiculo': veiculo})