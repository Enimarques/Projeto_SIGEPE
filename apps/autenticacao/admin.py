from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from django import forms
from apps.recepcao.models import Setor

class CustomUserCreationForm(UserCreationForm):
    setor = forms.ModelChoiceField(
        label='Setor/Gabinete',
        queryset=Setor.objects.filter(ativo=True),
        required=False,
        empty_label='Selecione um setor (apenas para assessores)...',
        help_text='Deixe vazio para tipos de usuário que não são assessores. Setores já atribuídos aparecerão indicados.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar todos os setores ativos
        self.fields['setor'].queryset = Setor.objects.filter(ativo=True).order_by('tipo', 'nome_vereador', 'nome_local')
    
    def clean_setor(self):
        setor = self.cleaned_data.get('setor')
        # Para novo usuário, só verificar se o setor já tem outro usuário
        if setor and setor.usuario:
            raise forms.ValidationError(
                f'Este setor já está atribuído ao usuário: {setor.usuario.username} ({setor.usuario.get_full_name() or setor.usuario.username})'
            )
        return setor
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Vincular ao setor se selecionado
            setor = self.cleaned_data.get('setor')
            if setor:
                # Limpar qualquer vinculação anterior do setor (por segurança)
                if setor.usuario:
                    Setor.objects.filter(id=setor.id).update(usuario=None)
                
                # Vincular ao novo usuário
                setor.usuario = user
                setor.save()
                
        return user

class CustomUserChangeForm(UserChangeForm):
    setor = forms.ModelChoiceField(
        label='Setor/Gabinete',
        queryset=Setor.objects.filter(ativo=True),
        required=False,
        empty_label='Selecione um setor (apenas para assessores)...',
        help_text='Deixe vazio para tipos de usuário que não são assessores. Setores já atribuídos aparecerão indicados.'
    )
    
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar todos os setores ativos ordenados
        self.fields['setor'].queryset = Setor.objects.filter(ativo=True).order_by('tipo', 'nome_vereador', 'nome_local')
        
        # Se o usuário já tem setor vinculado, selecionar ele
        if self.instance and self.instance.pk:
            try:
                # Buscar setor vinculado usando consulta direta
                setor_vinculado = Setor.objects.filter(usuario=self.instance).first()
                if setor_vinculado:
                    self.fields['setor'].initial = setor_vinculado
            except Exception:
                pass
    
    def clean_setor(self):
        setor = self.cleaned_data.get('setor')
        if setor and setor.usuario and setor.usuario != self.instance:
            raise forms.ValidationError(
                f'Este setor já está atribuído ao usuário: {setor.usuario.username} ({setor.usuario.get_full_name() or setor.usuario.username})'
            )
        return setor
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Limpar vinculações anteriores deste usuário
            from apps.recepcao.models import Setor
            Setor.objects.filter(usuario=user).update(usuario=None)
            
            # Vincular ao novo setor se selecionado
            setor = self.cleaned_data.get('setor')
            if setor:
                # Limpar vinculação anterior do setor (por segurança)
                if setor.usuario and setor.usuario != user:
                    setor.usuario = None
                    setor.save()
                
                setor.usuario = user
                setor.save()
                
        return user

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_groups', 'is_active', 'get_setor')
    list_filter = ('groups', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método save_model para garantir que a vinculação do setor seja salva.
        """
        # Primeiro salva o usuário
        super().save_model(request, obj, form, change)
        
        # Depois trata a vinculação do setor
        if hasattr(form, 'cleaned_data') and 'setor' in form.cleaned_data:
            setor = form.cleaned_data.get('setor')
            
            # Primeiro, limpar TODAS as vinculações anteriores deste usuário
            from apps.recepcao.models import Setor
            Setor.objects.filter(usuario=obj).update(usuario=None)
            
            # Vincular ao novo setor se selecionado
            if setor:
                # Garantir que o setor não tenha outro usuário vinculado
                if setor.usuario and setor.usuario != obj:
                    setor.usuario = None
                    setor.save()
                
                # Vincular o setor ao usuário atual
                setor.usuario = obj
                setor.save()

    def delete_model(self, request, obj):
        import logging
        logging.getLogger('audit').info(
            f"user={request.user.username} action=DELETE_USER target_user_id={obj.id} target_username='{obj.username}' ip={request.META.get('REMOTE_ADDR')}"
        )
        super().delete_model(request, obj)

    def get_groups(self, obj):
        groups = obj.groups.all()
        return ', '.join([group.name for group in groups])
    get_groups.short_description = 'Grupos'
    
    def get_setor(self, obj):
        try:
            # Use o método reverso da relação OneToOneField
            from apps.recepcao.models import Setor
            setor = Setor.objects.filter(usuario=obj).first()
            if setor:
                if setor.tipo in ['gabinete', 'gabinete_vereador']:
                    return f"Gabinete: {setor.nome_vereador}"
                else:
                    return f"Departamento: {setor.nome_local}"
            return '-'
        except Exception:
            return '-'
    get_setor.short_description = 'Setor'

    def get_fieldsets(self, request, obj=None):
        if not obj:  # Criando novo usuário
            return (
                (None, {'fields': ('username', 'password1', 'password2')}),
                ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
                ('Permissões', {'fields': ('is_active', 'groups')}),
                ('Setor/Gabinete', {'fields': ('setor',)}),
            )
        else:  # Editando usuário existente
            return (
                (None, {'fields': ('username', 'password')}),
                ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
                ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Setor/Gabinete', {'fields': ('setor',)}),
                ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
            )

# Desregistra o UserAdmin padrão e registra o CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Personaliza a exibição de grupos
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    
    def get_users_count(self, obj):
        count = obj.user_set.count()
        return format_html('<span>{} usuários</span>', count)
    get_users_count.short_description = 'Usuários no Grupo'

# Desregistra o GroupAdmin padrão e registra o CustomGroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# Register your models here.
