"""
Views para autenticação de usuários.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from ..services.auth_service import AuthenticationService
from ..forms.auth_forms import LoginForm, AssessorLoginForm, CustomPasswordResetForm, CustomSetPasswordForm

def login_sistema(request):
    """
    View para login no sistema principal.
    Utiliza o serviço de autenticação para validar o usuário.
    """
    # Se o usuário já está logado, redireciona para a página principal
    if request.user.is_authenticated:
        return redirect('main:home_sistema')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Usar o serviço de autenticação
            user = AuthenticationService.authenticate_user(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Atualizar o timestamp de último login
                AuthenticationService.update_last_login(user)
                
                # Pega a URL de redirecionamento do POST ou GET, ou usa a home como padrão
                next_url = request.POST.get('next') or request.GET.get('next') or 'main:home_sistema'
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    # Passa o next para o template para que ele possa incluir no formulário
    next_url = request.GET.get('next', '')
    return render(request, 'autenticacao/login_sistema.html', {
        'form': form,
        'title': 'Login - URUTAU',
        'next': next_url
    })

def login_assessor(request):
    """
    View para login de assessores.
    Utiliza o serviço de autenticação para validar o assessor.
    """
    # Se o usuário já está logado, redireciona para a página do gabinete
    if request.user.is_authenticated:
        if AuthenticationService.is_assessor(request.user):
            departamento = AuthenticationService.get_assessor_departamento(request.user)
            if departamento:
                return redirect('gabinetes:detalhes_gabinete', pk=departamento.id)
        return redirect('main:home_sistema')
        
    if request.method == 'POST':
        form = AssessorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Usar o serviço de autenticação
            user = AuthenticationService.authenticate_user(username=username, password=password)
            
            if user is not None and AuthenticationService.is_assessor(user):
                login(request, user)
                # Atualizar o timestamp de último login
                AuthenticationService.update_last_login(user)
                
                # Redirecionar para a página do gabinete
                departamento = AuthenticationService.get_assessor_departamento(user)
                if departamento:
                    messages.success(request, f'Bem-vindo, {user.first_name}!')
                    return redirect('gabinetes:detalhes_gabinete', pk=departamento.id)
                    
                # Se não tiver departamento, redireciona para a home
                return redirect('main:home_sistema')
            else:
                messages.error(request, 'Usuário ou senha inválidos ou não é um assessor.')
    else:
        form = AssessorLoginForm()
    
    return render(request, 'autenticacao/login_assessor.html', {
        'form': form,
        'title': 'Login de Assessor - URUTAU'
    })

@login_required
def logout_sistema(request):
    """View para logout do sistema."""
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_sistema')

@login_required
def logout_assessor(request):
    """View para logout de assessores."""
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_assessor')

# Views para recuperação de senha
class CustomPasswordResetView(PasswordResetView):
    """View personalizada para solicitação de redefinição de senha."""
    form_class = CustomPasswordResetForm
    template_name = 'autenticacao/password_reset_form.html'
    email_template_name = 'autenticacao/password_reset_email.html'
    success_url = reverse_lazy('autenticacao:password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    """View personalizada para confirmação de envio de email de redefinição."""
    template_name = 'autenticacao/password_reset_done.html'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """View personalizada para definição de nova senha."""
    form_class = CustomSetPasswordForm
    template_name = 'autenticacao/password_reset_confirm.html'
    success_url = reverse_lazy('autenticacao:password_reset_complete')
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """View personalizada para confirmação de redefinição de senha."""
    template_name = 'autenticacao/password_reset_complete.html' 