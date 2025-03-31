from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from apps.recepcao.models import Assessor

class UsuarioForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('assessor', 'Assessor')
    ]
    
    tipo_usuario = forms.ChoiceField(
        label='Tipo de Usuário',
        choices=TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_usuario'
        })
    )
    
    assessor = forms.ModelChoiceField(
        label='Assessor',
        queryset=Assessor.objects.filter(usuario__isnull=True, ativo=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_assessor'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_usuario', 'assessor']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Não escondemos mais o campo de assessor, isso será controlado via JavaScript
        # O campo será mostrado/escondido dependendo da seleção do tipo de usuário
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Adiciona o usuário ao grupo apropriado
            if self.cleaned_data['tipo_usuario'] == 'admin':
                grupo_admin = Group.objects.get(name='Administradores')
                grupo_admin.user_set.add(user)
            
            # Se for assessor, vincula ao assessor selecionado
            if self.cleaned_data['tipo_usuario'] == 'assessor' and self.cleaned_data['assessor']:
                assessor = self.cleaned_data['assessor']
                assessor.usuario = user
                assessor.save()
        
        return user