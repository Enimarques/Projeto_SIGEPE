"""
Decorators para controle de acesso.
"""
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

from ..services.auth_service import AuthenticationService

def admin_required(function):
    """
    Decorator para verificar se o usuário pertence ao grupo 'Administradores'.
    Usa o serviço de autenticação para verificar se o usuário é um administrador.
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
    Usa o serviço de autenticação para verificar se o usuário é assessor.
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
    Usa o serviço de autenticação para verificar se o usuário é assessor.
    Se o usuário for um assessor, redireciona para a página do gabinete vinculado.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_assessor(request.user):
            departamento = AuthenticationService.get_assessor_departamento(request.user)
            if departamento:
                messages.warning(request, 'Assessores não têm acesso a esta área do sistema.')
                return redirect('gabinetes:detalhes_gabinete', pk=departamento.id)
            else:
                messages.warning(request, 'Você não tem acesso a esta área do sistema.')
                return redirect('main:home_sistema')
        # Se não for assessor, permite o acesso
        return function(request, *args, **kwargs)
    return wrapper

def assessor_gabinete_access(function):
    """
    Decorator para verificar se o assessor tem acesso ao gabinete específico.
    Usa o serviço de autenticação para verificar o acesso.
    Se o gabinete não for o vinculado ao assessor, retorna 404.
    """
    def wrapper(request, *args, **kwargs):
        if not AuthenticationService.is_assessor(request.user):
            # Se não for assessor, permite o acesso normalmente
            return function(request, *args, **kwargs)
            
        # Verifica se o gabinete solicitado é o mesmo vinculado ao assessor
        if 'pk' in kwargs and not AuthenticationService.assessor_can_access_gabinete(request.user, kwargs['pk']):
            raise Http404("Gabinete não encontrado")
            
        return function(request, *args, **kwargs)
    return wrapper

def permission_required(permission_name):
    """
    Decorator para verificar se o usuário tem uma permissão específica.
    Usa o serviço de autenticação para verificar as permissões do usuário.
    
    Args:
        permission_name (str): Nome da permissão a ser verificada
        
    Returns:
        function: Decorator configurado para a permissão
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            permissions = AuthenticationService.get_user_permissions(request.user)
            if permission_name in permissions and permissions[permission_name]:
                return function(request, *args, **kwargs)
            messages.error(request, 'Você não tem permissão para realizar esta ação.')
            return redirect('main:home_sistema')
        return wrapper
    return decorator 