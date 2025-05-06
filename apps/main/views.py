from django.shortcuts import render
from apps.recepcao.models import Visita, Visitante, Assessor
from apps.veiculos.models import Veiculo
from apps.autenticacao.services.auth_service import AuthenticationService
from django.contrib.auth.models import User, Group

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
