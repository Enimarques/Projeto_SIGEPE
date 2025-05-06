"""
Views para gerenciamento de usuários.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..services.user_service import UserService
from ..utils.decorators import admin_required

@login_required
@admin_required
def lista_usuarios(request):
    """
    View para listar todos os usuários.
    """
    usuarios = UserService.get_all_users()
    return render(request, 'autenticacao/lista_usuarios.html', {
        'usuarios': usuarios,
        'title': 'Lista de Usuários - URUTAU'
    })

@login_required
@admin_required
def cadastro_usuario(request):
    """
    View para cadastro de novos usuários.
    Utiliza o serviço de usuário para criar um novo usuário.
    """
    if request.method == 'POST':
        result = UserService.create_user(request.POST)
        if result.success:
            messages.success(request, result.message)
            return redirect('autenticacao:lista_usuarios')
        else:
            messages.error(request, result.message)
            return render(request, 'autenticacao/cadastro_usuario.html', {
                'form': result.data.get('form', UserService.get_user_form()),
                'title': 'Cadastro de Usuário - URUTAU'
            })
    else:
        form = UserService.get_user_form()
        
    return render(request, 'autenticacao/cadastro_usuario.html', {
        'form': form,
        'title': 'Cadastro de Usuário - URUTAU'
    })

@login_required
@admin_required
def editar_usuario(request, pk):
    """
    View para editar um usuário existente.
    Utiliza o serviço de usuário para atualizar o usuário.
    """
    usuario = UserService.get_user_by_id(pk)
    
    if request.method == 'POST':
        result = UserService.update_user(pk, request.POST)
        if result.success:
            messages.success(request, result.message)
            return redirect('autenticacao:lista_usuarios')
        else:
            messages.error(request, result.message)
            return render(request, 'autenticacao/editar_usuario.html', {
                'form': result.data.get('form', UserService.get_user_form(usuario)),
                'usuario': usuario,
                'title': 'Editar Usuário - URUTAU'
            })
    else:
        form = UserService.get_user_form(usuario)
        
    return render(request, 'autenticacao/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'title': 'Editar Usuário - URUTAU'
    })

@login_required
@admin_required
def excluir_usuario(request, pk):
    """
    View para excluir um usuário.
    Utiliza o serviço de usuário para excluir o usuário.
    """
    usuario = UserService.get_user_by_id(pk)
    
    if request.method == 'POST':
        result = UserService.delete_user(pk)
        if result.success:
            messages.success(request, result.message)
        else:
            messages.error(request, result.message)
        return redirect('autenticacao:lista_usuarios')
        
    return render(request, 'autenticacao/confirmar_exclusao.html', {
        'usuario': usuario,
        'title': 'Excluir Usuário - URUTAU'
    })

@login_required
def perfil_usuario(request):
    """
    View para o usuário atual editar seu perfil.
    Utiliza o serviço de usuário para atualizar o perfil.
    """
    if request.method == 'POST':
        result = UserService.update_user_profile(request.user, request.POST)
        if result.success:
            messages.success(request, result.message)
        else:
            messages.error(request, result.message)
    
    form = UserService.get_user_profile_form(request.user)
    
    return render(request, 'autenticacao/perfil_usuario.html', {
        'form': form,
        'title': 'Meu Perfil - URUTAU'
    }) 