from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

def admin_required(function):
    """
    Decorator para verificar se o usuário pertence ao grupo 'Administradores'.
    Se não pertencer, redireciona para a página principal com uma mensagem de erro.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Administradores').exists():
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
        try:
            assessor = request.user.assessor
            if assessor.ativo:
                return function(request, *args, **kwargs)
            else:
                messages.error(request, 'Sua conta de assessor está desativada.')
                return redirect('main:home_sistema')
        except:
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('main:home_sistema')
    return wrapper

def block_assessor(function):
    """
    Decorator para bloquear o acesso de assessores a determinadas páginas.
    Se o usuário for um assessor, redireciona para a página do gabinete vinculado.
    """
    def wrapper(request, *args, **kwargs):
        try:
            # Verifica se o usuário é um assessor
            assessor = request.user.assessor
            # Se for assessor, redireciona para a página do gabinete vinculado
            messages.warning(request, 'Assessores não têm acesso a esta área do sistema.')
            return redirect('gabinetes:detalhes_gabinete', pk=assessor.departamento.id)
        except:
            # Se não for assessor, permite o acesso
            return function(request, *args, **kwargs)
    return wrapper

def assessor_gabinete_access(function):
    """
    Decorator para verificar se o assessor tem acesso ao gabinete específico.
    Se o gabinete não for o vinculado ao assessor, retorna 404.
    """
    def wrapper(request, *args, **kwargs):
        try:
            # Verifica se o usuário é um assessor
            assessor = request.user.assessor
            # Verifica se o gabinete solicitado é o mesmo vinculado ao assessor
            if 'pk' in kwargs and int(kwargs['pk']) != assessor.departamento.id:
                raise Http404("Gabinete não encontrado")
            return function(request, *args, **kwargs)
        except AttributeError:
            # Se não for assessor, permite o acesso normalmente
            return function(request, *args, **kwargs)
    return wrapper