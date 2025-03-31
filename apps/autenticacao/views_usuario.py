from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms_usuario import UsuarioForm
from .decorators import admin_required

@login_required
@admin_required
def cadastro_usuario(request):
    """View para cadastro de novos usuários no sistema"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('main:home_sistema')
    else:
        form = UsuarioForm()
    
    return render(request, 'autenticacao/cadastro_usuario.html', {
        'form': form,
        'title': 'Cadastro de Usuário - URUTAU'
    })

@login_required
@admin_required
def lista_usuarios(request):
    """View para listar todos os usuários do sistema"""
    users = User.objects.all().order_by('username')
    return render(request, 'autenticacao/lista_usuarios.html', {
        'users': users,
        'title': 'Lista de Usuários - URUTAU'
    })

@login_required
@admin_required
def editar_usuario(request, pk):
    """View para editar um usuário existente"""
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            return redirect('autenticacao:lista_usuarios')
    else:
        form = UsuarioForm(instance=user)
    
    return render(request, 'autenticacao/editar_usuario.html', {
        'form': form,
        'title': f'Editar Usuário {user.username} - URUTAU'
    })

@login_required
@admin_required
def excluir_usuario(request, pk):
    """View para excluir um usuário existente"""
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuário {user.username} excluído com sucesso!')
        return redirect('autenticacao:lista_usuarios')
    
    return render(request, 'autenticacao/excluir_usuario.html', {
        'user': user,
        'title': f'Excluir Usuário {user.username} - URUTAU'
    })