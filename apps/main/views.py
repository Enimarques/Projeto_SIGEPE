from django.shortcuts import render
from apps.recepcao.models import Visita, Visitante
from apps.veiculos.models import Veiculo

def home_sistema(request):
    # Dados da Recepção
    visitas_em_andamento = Visita.objects.filter(data_saida__isnull=True).count()
    total_visitantes = Visitante.objects.count()
    
    # Dados de Veículos
    veiculos_no_estacionamento = Veiculo.objects.filter(status='presente').count()
    total_veiculos = Veiculo.objects.count()
    
    return render(request, 'main/home_sistema.html', {
        'title': 'Home - URUTAU',
        'visitas_em_andamento': visitas_em_andamento,
        'total_visitantes': total_visitantes,
        'veiculos_no_estacionamento': veiculos_no_estacionamento,
        'total_veiculos': total_veiculos
    })
