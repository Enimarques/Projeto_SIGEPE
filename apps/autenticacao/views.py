from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .services.auth_service import AuthenticationService

# Create your views here.

def login_sistema(request):
    # Se o usuário já está logado, redireciona baseado no tipo
    if request.user.is_authenticated:
        return _redirect_user_by_type(request.user)
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = AuthenticationService.authenticate_user(username, password)
            
            if user is not None:
                login(request, user)
                AuthenticationService.update_last_login(user)
                
                # Se tem next URL específica, usa ela, senão redireciona por tipo
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    messages.success(request, f'Bem-vindo, {user.first_name}!')
                    return redirect(next_url)
                else:
                    messages.success(request, f'Bem-vindo, {user.first_name}!')
                    return _redirect_user_by_type(user)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    # Passa o next para o template para que ele possa incluir no formulário
    next_url = request.GET.get('next', '')
    return render(request, 'autenticacao/login_sistema.html', {
        'form': form,
        'title': 'Login - SIGEPE',
        'next': next_url
    })

def _redirect_user_by_type(user):
    """Redireciona o usuário baseado no seu tipo/grupo"""
    # Verificar se é assessor (tem setor vinculado)
    if AuthenticationService.is_assessor(user):
        # Assessores vão para o home ao invés do gabinete
        return redirect('main:home_sistema')
    
    # Verificar se é agente de guarita
    if user.groups.filter(name='Agente_Guarita').exists():
        return redirect('veiculos:home_veiculos')
    
    # Para administradores e recepcionistas, vai para a home geral
    return redirect('main:home_sistema')

@login_required
def logout_sistema(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_sistema')
