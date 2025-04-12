from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms_assessor import AssessorLoginForm, AssessorSetPasswordForm
from apps.recepcao.models import Assessor
import uuid
from django.utils import timezone
from datetime import timedelta
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

def login_assessor(request):
    # Se o usuário já está logado, redireciona para a página principal
    if request.user.is_authenticated:
        # Verifica se o usuário é um assessor
        try:
            assessor = request.user.assessor
            return redirect('gabinetes:detalhes_gabinete', pk=assessor.departamento.id)
        except:
            # Se não for assessor, redireciona para a página principal
            return redirect('main:home_sistema')
        
    if request.method == 'POST':
        form = AssessorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Verifica se o usuário é um assessor
                try:
                    assessor = user.assessor
                    if not assessor.ativo:
                        messages.error(request, 'Sua conta está desativada. Entre em contato com o administrador.')
                        return render(request, 'autenticacao/login_assessor.html', {
                            'form': form,
                            'title': 'Login Assessor - URUTAU'
                        })
                    
                    login(request, user)
                    messages.success(request, f'Bem-vindo, {user.first_name}!')
                    return redirect('gabinetes:detalhes_gabinete', pk=assessor.departamento.id)
                except:
                    messages.error(request, 'Este usuário não está vinculado a um assessor.')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AssessorLoginForm()
    
    return render(request, 'autenticacao/login_assessor.html', {
        'form': form,
        'title': 'Login Assessor - URUTAU'
    })

@login_required
def logout_assessor(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('autenticacao:login_assessor')

def set_password_assessor(request, token):
    signer = TimestampSigner()
    token_valid = True
    error_message = None
    assessor_id = None
    
    try:
        # Verificar se o token é válido e não expirou (validade de 24 horas)
        assessor_id = signer.unsign(token, max_age=86400)  # 24 horas em segundos
    except SignatureExpired:
        token_valid = False
        error_message = "O link para definição de senha expirou. Por favor, solicite um novo link."
    except BadSignature:
        token_valid = False
        error_message = "O link para definição de senha é inválido."
    
    if token_valid and assessor_id:
        try:
            assessor = Assessor.objects.get(id=assessor_id)
            
            if request.method == 'POST':
                form = AssessorSetPasswordForm(request.POST)
                if form.is_valid():
                    # Se o assessor já tem um usuário, atualiza a senha
                    if assessor.usuario:
                        user = assessor.usuario
                        user.set_password(form.cleaned_data['password2'])
                        user.save()
                    else:
                        # Cria um novo usuário para o assessor
                        username = f"assessor_{assessor.id}"
                        # Verifica se o username já existe
                        if User.objects.filter(username=username).exists():
                            username = f"assessor_{assessor.id}_{uuid.uuid4().hex[:6]}"
                        
                        # Cria o usuário
                        user = User.objects.create_user(
                            username=username,
                            email=assessor.email,
                            password=form.cleaned_data['password2'],
                            first_name=assessor.nome.split()[0],
                            last_name=' '.join(assessor.nome.split()[1:]) if len(assessor.nome.split()) > 1 else ''
                        )
                        
                        # Adiciona ao grupo de assessores (se existir)
                        assessor_group, created = Group.objects.get_or_create(name='Assessores')
                        user.groups.add(assessor_group)
                        
                        # Vincula o usuário ao assessor
                        assessor.usuario = user
                        assessor.save()
                    
                    messages.success(request, 'Senha definida com sucesso! Agora você pode fazer login.')
                    return redirect('autenticacao:login_assessor')
            else:
                form = AssessorSetPasswordForm(initial={'token': token})
                
            return render(request, 'autenticacao/set_password_assessor.html', {
                'form': form,
                'token': token,
                'token_valid': token_valid,
                'title': 'Definir Senha - URUTAU'
            })
            
        except Assessor.DoesNotExist:
            token_valid = False
            error_message = "Assessor não encontrado."
    
    # Se chegou aqui, o token é inválido ou expirou
    return render(request, 'autenticacao/set_password_assessor.html', {
        'token_valid': token_valid,
        'error_message': error_message,
        'title': 'Definir Senha - URUTAU'
    })

def generate_password_token(assessor_id):
    """Gera um token assinado para redefinição de senha"""
    signer = TimestampSigner()
    return signer.sign(str(assessor_id))