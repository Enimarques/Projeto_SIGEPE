from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_groups', 'is_active', 'get_setor')
    list_filter = ('groups', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def get_groups(self, obj):
        groups = obj.groups.all()
        return ', '.join([group.name for group in groups])
    get_groups.short_description = 'Grupos'
    
    def get_setor(self, obj):
        try:
            return obj.setor_responsavel.nome
        except:
            return '-'
    get_setor.short_description = 'Setor'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                (None, {'fields': ('username', 'password1', 'password2')}),
                ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
                ('Permissões', {'fields': ('is_active', 'groups')}),
            )
        return (
            (None, {'fields': ('username', 'password')}),
            ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissões', {'fields': ('is_active', 'groups')}),
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
