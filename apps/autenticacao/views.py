from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.

def login_sistema(request):
    if request.user.is_authenticated:
        return redirect('recepcao:home_sistema')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'recepcao:home_sistema')
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'autenticacao/login_sistema.html', {
        'form': form,
        'title': 'Login - URUTAU'
    })

@login_required
def logout_sistema(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('recepcao:login_sistema')
