from django.shortcuts import render, redirect #importando funções de renderização e redirecionamento
from django.contrib.auth import login, authenticate #importando funções de autenticação
from .forms import RegisterForm, VisitaForm, FimVisitaForm  #importando o formulario de registro
from .models import Visita #importando o modelo de 
from django.utils import timezone #importando a função de pegar a data e hora atual
from django.contrib import messages #importando a função de mensagens
from django.shortcuts import get_object_or_404 #importando a função de pegar um objeto 

def home(request):
    return render(request, 'home.html')

def cadastrar_visitante(request):
    if request.method == 'POST': #se o metodo for post (enviar informações)
        form = RegisterForm(request.POST, request.FILES) #cria um formulario com os dados do post
        if form.is_valid():
          form.save() #salva o formulario
          messages.success(request, 'Visitante registrado com sucesso!')
          return redirect('home')
    else:
        form = RegisterForm() #se não for post, cria um formulario vazio
    return render(request, 'registro/cadastrar_visitante.html', {'form': form}) #retorna o formulario na tela


def registrar_visita(request):
    if request.method == 'POST': #LOGICA PARA REGISTRAR VISITAS
        form = VisitaForm(request.POST) #cria um formulario com os dados do post
        if form.is_valid():
          form.save() #salva o formulario
          messages.success(request, 'Visita registrada com sucesso!')
          return redirect('home')
    else:
        form = VisitaForm() #se não for post, cria um formulario vazio
    return render(request, 'visitas/registrar_visita.html', {'form': form}) #retorna o formulario na tela

def fim_visita(request): #LOGICA PARA FINALIZAR VISITAS
    if request.method == 'POST': #se o metodo for post (enviar informações)
        form = FimVisitaForm(request.POST) #cria um formulario com os dados do post
        if form.is_valid():
          visita = form.cleaned_data['visita']
          visita.data_saida = timezone.now() #pega a data e hora atual pra registrar saida
          visita.save() #salva a visita
          messages.success(request, f'Visita de {visita.visitante} finalizada com sucesso!')
          return redirect('home')
    else:
        form = FimVisitaForm()
    return render(request, 'visitas/fim_visita.html', {'form': form}) #retorna a pagina de finalização de visita