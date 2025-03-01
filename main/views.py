from django.shortcuts import render, redirect #importando funções de renderização e redirecionamento
from django.contrib.auth import login, authenticate #importando funções de autenticação
from .forms import RegisterForm, VisitaForm  #importando o formulario de registro
from .models import Visita #importando o modelo de visita
from django.utils import timezone #importando a função de pegar a data e hora atual

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST': #se o metodo for post (enviar informações)
        form = RegisterForm(request.POST) #cria um formulario com os dados do post
        if form.is_valid():
          user = form.save() #salva o formulario
          login(request, user) #faz o login do usuario automaticamente mas não é necessário
          return redirect('home')
    else:
        form = RegisterForm() #se não for post, cria um formulario vazio
    return render(request, 'registro/registro.html', {'form': form}) #retorna o formulario na tela


def registrar_visita(request):
    if request.method == 'POST': #LOGICA PARA REGISTRAR VISITAS
        form = VisitaForm(request.POST) #cria um formulario com os dados do post
        if form.is_valid():
          form.save() #salva o formulario
          return redirect('home')
    else:
        form = VisitaForm() #se não for post, cria um formulario vazio
    return render(request, 'visitas/registrar_visita.html', {'form': form}) #retorna o formulario na tela

def fim_visita(request, visita_id): #LOGICA PARA FINALIZAR VISITAS
    visita = Visita.objects.get(id=visita_id) #pega a visita pelo id
    if request.method == 'POST': #se o metodo for post (enviar informações)
        visita.data_saida = timezone.now() #pega a data e hora atual
        visita.save() #salva a visita
        return redirect('home') #retorna para a home
    return render(request, 'visitas/fim_visita.html', {'visita': visita}) #retorna a pagina de finalização de visita
