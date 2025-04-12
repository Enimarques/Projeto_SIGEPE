from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .forms_usuario import UsuarioForm
from .decorators import admin_required

@login_required
@admin_required
def cadastro_usuario(request):
    """View para cadastro de novos usuários"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('autenticacao:lista_usuarios')
    else:
        form = UsuarioForm()
        
    return render(request, 'autenticacao/cadastro_usuario.html', {'form': form})

@login_required
@admin_required
def lista_usuarios(request):
    """View para listar todos os usuários"""
    usuarios = User.objects.all().order_by('username')
    return render(request, 'autenticacao/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@admin_required
def editar_usuario(request, pk):
    """View para editar um usuário existente"""
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('autenticacao:lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
        
    return render(request, 'autenticacao/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@admin_required
def excluir_usuario(request, pk):
    """View para excluir um usuário"""
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('autenticacao:lista_usuarios')
    return render(request, 'autenticacao/excluir_usuario.html', {'usuario': usuario})