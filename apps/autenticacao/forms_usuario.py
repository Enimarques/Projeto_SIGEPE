from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from apps.recepcao.models import Setor
from django.db.models import Q

class UsuarioForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('assessor', 'Assessor'),
        ('agente_guarita', 'Agente Guarita'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    tipo_usuario = forms.ChoiceField(
        label='Tipo de Usuário',
        choices=TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_usuario'
        })
    )
    
    setor = forms.ModelChoiceField(
        label='Setor/Gabinete',
        queryset=Setor.objects.filter(usuario__isnull=True, ativo=True),
        required=False,
        empty_label='Selecione um setor...',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_setor'
        }),
        help_text='Obrigatório apenas para usuários do tipo Assessor'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_usuario', 'setor']
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
            
            # Se estiver editando, incluir o setor atual na queryset se ele já tiver um
            if hasattr(self.instance, 'setor_responsavel') and self.instance.setor_responsavel:
                current_setor = self.instance.setor_responsavel
                self.fields['setor'].queryset = Setor.objects.filter(
                    Q(usuario__isnull=True, ativo=True) | Q(id=current_setor.id)
                )
                self.fields['setor'].initial = current_setor
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_usuario = cleaned_data.get('tipo_usuario')
        setor = cleaned_data.get('setor')
        
        # Validar se assessor tem setor selecionado
        if tipo_usuario == 'assessor' and not setor:
            raise forms.ValidationError('É obrigatório selecionar um setor para usuários do tipo Assessor.')
        
        # Validar se setor foi selecionado para outros tipos (não deveria)
        if tipo_usuario != 'assessor' and setor:
            raise forms.ValidationError('Apenas usuários do tipo Assessor podem ter setor vinculado.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Se for um usuário existente e as senhas estiverem vazias, não altere a senha
        if self.instance.pk and not self.cleaned_data.get('password1'):
            pass  # Não altera a senha
        else:
            # Garantir que a senha seja definida para novos usuários
            if not user.password or user.password.startswith('!'):  # Senha não definida ou inválida
                user.set_password(self.cleaned_data.get('password1'))
        
        if commit:
            user.save()
            
            # Adiciona o usuário ao grupo apropriado
            if self.cleaned_data['tipo_usuario'] == 'admin':
                # Torna o usuário administrador um superusuário para garantir acesso completo
                user.is_superuser = True
                user.is_staff = True
                user.save()
                
                # Desvincular setor se existir (admin não deveria ter setor)
                if hasattr(user, 'setor_responsavel') and user.setor_responsavel:
                    setor_anterior = user.setor_responsavel
                    setor_anterior.usuario = None
                    setor_anterior.save()
                
                # Adiciona ao grupo de Administradores para manter compatibilidade
                grupo_admin, created = Group.objects.get_or_create(name='Administradores')
                grupo_admin.user_set.add(user)
                
                # Remover do grupo de assessores, se estiver nele
                grupo_assessor, created = Group.objects.get_or_create(name='Assessores')
                if user in grupo_assessor.user_set.all():
                    grupo_assessor.user_set.remove(user)
            
            # Se for assessor, vincula ao assessor selecionado
            elif self.cleaned_data['tipo_usuario'] == 'assessor':
                # Garante que não é um superusuário (por segurança)
                if user.is_superuser:
                    user.is_superuser = False
                    user.save()
                
                # Remover do grupo de administradores, se estiver nele
                grupo_admin, created = Group.objects.get_or_create(name='Administradores')
                if user in grupo_admin.user_set.all():
                    grupo_admin.user_set.remove(user)
                
                # Adiciona ao grupo de assessores
                grupo_assessor, created = Group.objects.get_or_create(name='Assessores')
                grupo_assessor.user_set.add(user)
                
                # Vincula ao setor, se selecionado
                if self.cleaned_data['setor']:
                    # Desvincular setor anterior se existir
                    if hasattr(user, 'setor_responsavel') and user.setor_responsavel:
                        setor_anterior = user.setor_responsavel
                        setor_anterior.usuario = None
                        setor_anterior.save()
                    
                    # Vincular ao novo setor
                    setor = self.cleaned_data['setor']
                    setor.usuario = user
                    setor.save()
            
            elif self.cleaned_data['tipo_usuario'] == 'agente_guarita':
                # Desvincular setor se existir (não-assessor não pode ter setor)
                if hasattr(user, 'setor_responsavel') and user.setor_responsavel:
                    setor_anterior = user.setor_responsavel
                    setor_anterior.usuario = None
                    setor_anterior.save()
                
                grupo_guarita, created = Group.objects.get_or_create(name='Agente_Guarita')
                grupo_guarita.user_set.add(user)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                # Remove de outros grupos se necessário
                grupo_admin, created = Group.objects.get_or_create(name='Administradores')
                if user in grupo_admin.user_set.all():
                    grupo_admin.user_set.remove(user)
                grupo_assessor, created = Group.objects.get_or_create(name='Assessores')
                if user in grupo_assessor.user_set.all():
                    grupo_assessor.user_set.remove(user)
                grupo_recepcionista, created = Group.objects.get_or_create(name='Recepcionista')
                if user in grupo_recepcionista.user_set.all():
                    grupo_recepcionista.user_set.remove(user)
            
            elif self.cleaned_data['tipo_usuario'] == 'recepcionista':
                # Desvincular setor se existir (não-assessor não pode ter setor)
                if hasattr(user, 'setor_responsavel') and user.setor_responsavel:
                    setor_anterior = user.setor_responsavel
                    setor_anterior.usuario = None
                    setor_anterior.save()
                
                grupo_recepcionista, created = Group.objects.get_or_create(name='Recepcionista')
                grupo_recepcionista.user_set.add(user)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                # Remove de outros grupos se necessário
                grupo_admin, created = Group.objects.get_or_create(name='Administradores')
                if user in grupo_admin.user_set.all():
                    grupo_admin.user_set.remove(user)
                grupo_assessor, created = Group.objects.get_or_create(name='Assessores')
                if user in grupo_assessor.user_set.all():
                    grupo_assessor.user_set.remove(user)
                grupo_guarita, created = Group.objects.get_or_create(name='Agente_Guarita')
                if user in grupo_guarita.user_set.all():
                    grupo_guarita.user_set.remove(user)
        
        return user