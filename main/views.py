from django.shortcuts import render, redirect, get_object_or_404
from main.models import Visita, Visitante #importando funções de renderização e redirecionamento
from .forms import RegisterForm, VisitaForm, FimVisitaForm  #importando o formulario de registro
from django.utils import timezone #importando a função de pegar a data e hora atual
from django.contrib import messages #importando a função de mensagens
#from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    return render(request, 'home.html')

def recepcao(request):
    return render(request, 'recepcao.html')

def estacionamento(request):
    return render(request, 'estacionamento.html')

def cadastrar_visitante(request):
    if request.method == 'POST': #se o metodo for post (enviar informações)
        form = RegisterForm(request.POST, request.FILES) #cria um formulario com os dados do post
        if form.is_valid():
          form.save() #salva o formulario
          messages.success(request, 'Visitante registrado com sucesso!')
          return redirect('recepcao')
    else:
        form = RegisterForm() #se não for post, cria um formulario vazio
    return render(request, 'registro/cadastrar_visitante.html', {'form': form}) #retorna o formulario na tela


def registrar_visita(request):
    if request.method == 'POST': #LOGICA PARA REGISTRAR VISITAS
        form = VisitaForm(request.POST) #cria um formulario com os dados do post
        if 'buscar' in request.POST: #se o botão de buscar for clicado
            if form.is_valid():
                cpf = form.cleaned_data['cpf']
                try:
                    visitante = Visitante.objects.get(CPF=cpf) #tenta pegar o visitante pelo cpf
                    form.fields['nome_visitante'].initial = visitante.nome_completo #preenche o campo de nome do visitante
                except Visitante.DoesNotExist: #se o visitante não existir
                    messages.error(request, 'Visitante não encontrado!')
                    return redirect(f'/cadastrar_visitante/?cpf={cpf}') #redireciona para a pagina de cadastro de visitante
        elif form.is_valid():
          cpf = form.cleaned_data['cpf'] #pega o cpf do formulario
          try:
            visitante = Visitante.objects.get(CPF=cpf) #tenta pegar o visitante pelo cpf
            visita = form.save(commit=False) #cria uma visita com os dados do formulario               
            visita.visitante = visitante #associa o visitante a visita
            visita.data_entrada = timezone.now() #pega a data e hora atual pra registrar entrada          
            visita.save() #salva a visita
            messages.success(request, 'Visita registrada com sucesso!')
            return redirect('recepcao')
          except Visitante.DoesNotExist: #se o visitante não existir
            messages.error(request, 'Visitante não encontrado!')
            return redirect(f'/cadastrar_visitante/?cpf={cpf}') #redireciona para a pagina de cadastro de visitante

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
          return redirect('recepcao')
    else:
        form = FimVisitaForm()
    return render(request, 'visitas/fim_visita.html', {'form': form}) #retorna a pagina de finalização de visita

'''def is_estacionamento(user):
    """Verifica se o usuário pertence ao grupo 'Estacionamento'"""
    return user.groups.filter(name='Estacionamento').exists()

@login_required
@user_passes_test(is_estacionamento)
def home_estacionamento(request):
    return render(request, 'home_estacionamento.html')  # Criar este template'''