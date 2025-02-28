from django.shortcuts import render, redirect #importando funções de renderização e redirecionamento
from django.contrib.auth import login, authenticate #importando funções de autenticação
from .forms import RegisterForm  #importando o formulario de registro

def register(request):
    if request.method == 'POST': #se o metodo for post (enviar informações)
        form = RegisterForm(request.POST) #cria um formulario com os dados do post
        if form.is_valid():
          user = form.save() #salva o formulario
          login(request, user) #faz o login do usuario
          return redirect('home')
    else:
        form = RegisterForm() #se não for post, cria um formulario vazio
    return render(request, 'registration/register.html', {'form': form}) #retorna o formulario na tela
        

