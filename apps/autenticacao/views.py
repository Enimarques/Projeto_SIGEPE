from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.

def login_sistema(request):
    # Se o usuário já está logado, redireciona para a página principal
    if request.user.is_authenticated:
        return redirect('main:home_sistema')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
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

@login_required
def logout_sistema(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_sistema')
