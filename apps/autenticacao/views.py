from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_sistema(request):
    if request.user.is_authenticated:
        return redirect('main:home_sistema')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a) ao URUTAU, {user.username}!')
                next_url = request.GET.get('next', 'main:home_sistema')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'autenticacao/login_sistema.html', {
        'form': form,
        'title': 'Login - URUTAU'
    })

@login_required
def logout_sistema(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_sistema')
