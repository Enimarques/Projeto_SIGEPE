from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme sua senha',
        }   #muda o nome dos campos pra portugues
        help_texts = {
            'username': None,
        } #pra nao aparecer texto de ajuda
        
        