from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='autenticacao:login_sistema')
def home_sistema(request):
    return render(request, 'main/home_sistema.html')
