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
        
        # Torna os campos de senha não obrigatórios ao editar um usuário existente
        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Se for um usuário existente e as senhas estiverem vazias, não altere a senha
        if self.instance.pk and not self.cleaned_data.get('password1'):
            pass  # Não altera a senha
        
        if commit:
            user.save()
            
            # Adiciona o usuário ao grupo apropriado
            if self.cleaned_data['tipo_usuario'] == 'admin':
                # Torna o usuário administrador um superusuário para garantir acesso completo
                user.is_superuser = True
                user.is_staff = True
                user.save()
                
                # Adiciona ao grupo de Administradores para manter compatibilidade
                grupo_admin = Group.objects.get(name='Administradores')
                grupo_admin.user_set.add(user)
                
                # Remover do grupo de assessores, se estiver nele
                grupo_assessor = Group.objects.get(name='Assessores')
                if user in grupo_assessor.user_set.all():
                    grupo_assessor.user_set.remove(user)
            
            # Se for assessor, vincula ao assessor selecionado
            elif self.cleaned_data['tipo_usuario'] == 'assessor':
                # Garante que não é um superusuário (por segurança)
                if user.is_superuser:
                    user.is_superuser = False
                    user.save()
                
                # Remover do grupo de administradores, se estiver nele
                grupo_admin = Group.objects.get(name='Administradores')
                if user in grupo_admin.user_set.all():
                    grupo_admin.user_set.remove(user)
                
                # Adiciona ao grupo de assessores
                grupo_assessor = Group.objects.get(name='Assessores')
                grupo_assessor.user_set.add(user)
                
                # Vincula ao assessor, se selecionado
                if self.cleaned_data['assessor']:
                    assessor = self.cleaned_data['assessor']
                    assessor.usuario = user
                    assessor.save()
        
        return user