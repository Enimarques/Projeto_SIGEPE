from django.shortcuts import render, redirect
from apps.recepcao.models import Visita, Visitante, Setor
from apps.veiculos.models import Veiculo
from apps.autenticacao.services.auth_service import AuthenticationService
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

@login_required(login_url='autenticacao:login_sistema')
def home_sistema(request):
    user = request.user
    user_groups = [g.name for g in user.groups.all()]
    is_guarita = 'Agente_Guarita' in user_groups
    is_assessor = AuthenticationService.is_assessor(user)
    is_admin = AuthenticationService.is_admin(user)
    is_recepcionista = AuthenticationService.is_recepcionista(user)

    # Redirecionar automaticamente apenas para alguns tipos específicos
    redirect_param = request.GET.get('redirect', 'true')
    if redirect_param.lower() != 'false':
        # Agentes de guarita vão para o módulo de veículos
        if is_guarita:
            return redirect('veiculos:home_veiculos')
        
        # Assessores ficam no home (não redirecionam mais automaticamente)
        # Admins e recepcionistas também ficam no home

    context = {'title': 'Home - SIGEPE'}

    if is_guarita:
        # Home específica para Agente de Guarita
        context['veiculos_no_estacionamento'] = Veiculo.objects.filter(status='presente').count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['is_guarita'] = True
        context['is_assessor'] = False
        context['is_admin'] = False
        context['is_recepcionista'] = False
        
        # Estatísticas específicas para guarita
        hoje = timezone.now().date()
        context['veiculos_entraram_hoje'] = Veiculo.objects.filter(
            historico__data_entrada__date=hoje
        ).distinct().count()
        context['veiculos_sairam_hoje'] = Veiculo.objects.filter(
            historico__data_saida__date=hoje
        ).distinct().count()
        
    elif is_assessor:
        # Home específica para Assessor
        try:
            setor = user.setor_responsavel
            
            # Estatísticas do gabinete/departamento do assessor
            hoje = timezone.now().date()
            context['visitas_hoje_gabinete'] = Visita.objects.filter(
                setor=setor,
                data_entrada__date=hoje
            ).count()
            
            context['visitas_em_andamento_gabinete'] = Visita.objects.filter(
                setor=setor,
                data_saida__isnull=True
            ).count()
            
            context['total_visitas_gabinete'] = Visita.objects.filter(
                setor=setor
            ).count()
            
            # Dados do departamento
            context['departamento'] = setor
            context['setor'] = setor
            
            # Verificar se é gabinete ou departamento
            context['is_gabinete'] = setor.tipo in ['gabinete', 'gabinete_vereador']
            context['is_departamento'] = setor.tipo == 'departamento'
            
        except:
            # Fallback se não conseguir obter dados do setor
            context['visitas_hoje_gabinete'] = 0
            context['visitas_em_andamento_gabinete'] = 0
            context['total_visitas_gabinete'] = 0
            
        context['is_guarita'] = False
        context['is_assessor'] = True
        context['is_admin'] = False
        context['is_recepcionista'] = False
        
    elif is_recepcionista:
        # Home específica para Recepcionista
        hoje = timezone.now().date()
        context['visitas_em_andamento'] = Visita.objects.filter(data_saida__isnull=True).count()
        context['total_visitantes'] = Visitante.objects.count()
        context['visitas_hoje'] = Visita.objects.filter(data_entrada__date=hoje).count()
        context['visitantes_hoje'] = Visitante.objects.filter(
            visita__data_entrada__date=hoje
        ).distinct().count()
        
        context['is_guarita'] = False
        context['is_assessor'] = False
        context['is_admin'] = False
        context['is_recepcionista'] = True
        
    else:
        # Home para Administradores (padrão)
        hoje = timezone.now().date()
        context['visitas_em_andamento'] = Visita.objects.filter(data_saida__isnull=True).count()
        context['total_visitantes'] = Visitante.objects.count()
        context['veiculos_no_estacionamento'] = Veiculo.objects.filter(status='presente').count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['visitas_hoje'] = Visita.objects.filter(data_entrada__date=hoje).count()
        context['total_gabinetes'] = Setor.objects.filter(tipo='gabinete').count()
        context['total_departamentos'] = Setor.objects.filter(tipo='departamento').count()
        
        context['is_guarita'] = False
        context['is_assessor'] = False
        context['is_admin'] = True
        context['is_recepcionista'] = False

    return render(request, 'main/home_sistema.html', context)
