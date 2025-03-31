from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class AssessorLoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

class AssessorSetPasswordForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua nova senha',
            'autofocus': True
        }),
        help_text='A senha deve ter pelo menos 8 caracteres e conter letras e números.'
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite novamente sua senha'
        })
    )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('As senhas não coincidem.')
        
        try:
            validate_password(password2)
        except ValidationError as error:
            self.add_error('password2', error)
            
        return password2