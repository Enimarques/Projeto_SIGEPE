from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from .services.auth_service import AuthenticationService

def admin_required(function):
    """
    Decorator para verificar se o usuário pertence ao grupo 'Administradores'.
    Se não pertencer, redireciona para a página principal com uma mensagem de erro.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_admin(request.user):
            return function(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('main:home_sistema')
    return wrapper

def assessor_required(function):
    """
    Decorator para verificar se o usuário é um assessor.
    Se não for, redireciona para a página principal com uma mensagem de erro.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_assessor(request.user):
            return function(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('main:home_sistema')
    return wrapper

def block_assessor(function):
    """
    Decorator para bloquear o acesso de assessores a determinadas páginas.
    Se o usuário for um assessor, redireciona para a home com mensagem.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_assessor(request.user):
            messages.warning(request, 'Assessores não têm acesso a esta área do sistema.')
            return redirect('main:home_sistema')
        return function(request, *args, **kwargs)
    return wrapper

def assessor_gabinete_access(function):
    """
    Decorator para verificar se o assessor tem acesso ao gabinete específico.
    Se o gabinete não for o vinculado ao assessor, retorna 404.
    """
    def wrapper(request, *args, **kwargs):
        if 'pk' in kwargs and not AuthenticationService.assessor_can_access_gabinete(request.user, kwargs['pk']):
            raise Http404("Gabinete não encontrado")
        return function(request, *args, **kwargs)
    return wrapper

def assessor_own_gabinete_only(function):
    """
    Decorator para restringir assessores apenas ao seu próprio gabinete/departamento.
    Se o assessor tentar acessar outro gabinete, redireciona para o seu próprio.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_assessor(request.user):
            try:
                setor = request.user.setor_responsavel
                if setor:
                    # Se estiver tentando acessar um gabinete específico que não é o seu
                    if 'pk' in kwargs and int(kwargs['pk']) != setor.id:
                        if setor.tipo in ['gabinete', 'gabinete_vereador']:
                            messages.warning(request, f'Você só pode acessar informações do seu próprio gabinete.')
                            return redirect('gabinetes:detalhes_gabinete', pk=setor.id)
                        else:
                            messages.warning(request, f'Você só pode acessar informações do seu próprio departamento.')
                            return redirect('recepcao:detalhes_departamento', departamento_id=setor.id)
                else:
                    messages.error(request, 'Assessor não tem setor atribuído.')
                    return redirect('main:home_sistema')
            except Exception as e:
                messages.error(request, 'Erro ao verificar permissões do assessor.')
                return redirect('main:home_sistema')
        return function(request, *args, **kwargs)
    return wrapper

def agente_guarita_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Agente_Guarita').exists():
            return function(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('main:home_sistema')
    return wrapper

def agente_guarita_or_admin_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name__in=['Agente_Guarita', 'Administradores']).exists():
            return function(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('main:home_sistema')
    return wrapper

def block_recepcionista(function):
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_recepcionista(request.user):
            messages.error(request, 'Recepcionistas não têm acesso a esta área do sistema.')
            return redirect('main:home_sistema')
        return function(request, *args, **kwargs)
    return wrapper

def admin_or_recepcionista_only(function):
    """
    Decorator para permitir acesso apenas a administradores e recepcionistas.
    Bloqueia assessores e agentes de guarita, mas permite que assessores vejam 
    seu próprio gabinete.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        # Permite admin e recepcionista
        if AuthenticationService.is_admin(user) or AuthenticationService.is_recepcionista(user):
            return function(request, *args, **kwargs)
        
        # Para assessores, permite apenas acesso ao próprio gabinete/setor
        if AuthenticationService.is_assessor(user):
            # Se a view tem pk e é o setor do assessor, permite
            if 'pk' in kwargs:
                try:
                    setor_id = int(kwargs['pk'])
                    if user.setor_responsavel and user.setor_responsavel.id == setor_id:
                        return function(request, *args, **kwargs)
                except (ValueError, AttributeError):
                    pass
            
            # Senão, bloqueia com mensagem
            messages.warning(request, 'Você só pode acessar informações do seu próprio setor.')
            return redirect('main:home_sistema')
        
        # Bloqueia outros tipos
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('main:home_sistema')
    return wrapper

def assessor_or_admin_required(function):
    """
    Decorator para permitir acesso a assessores (apenas seu setor) e administradores.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        if AuthenticationService.is_admin(user) or AuthenticationService.is_assessor(user):
            return function(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('main:home_sistema')
    return wrapper