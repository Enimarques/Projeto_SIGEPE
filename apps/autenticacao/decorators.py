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
    Se o usuário for um assessor, redireciona para a página do gabinete vinculado.
    """
    def wrapper(request, *args, **kwargs):
        if AuthenticationService.is_assessor(request.user):
            assessor = request.user.assessor
            messages.warning(request, 'Assessores não têm acesso a esta área do sistema.')
            return redirect('gabinetes:detalhes_gabinete', pk=assessor.departamento.id)
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