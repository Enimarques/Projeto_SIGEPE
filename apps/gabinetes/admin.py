from django.contrib import admin
from django.utils import timezone

# Importando o modelo Gabinete
try:
    from .models import Gabinete
    
    # Classe de administração para o modelo Gabinete
    class GabineteAdmin(admin.ModelAdmin):
        list_display = ('nome', 'vereador', 'setor', 'telefone', 'email')
        list_filter = ('vereador',)
        search_fields = ('nome', 'vereador', 'setor__nome')
        readonly_fields = ('data_criacao', 'data_atualizacao')
        
        fieldsets = (
            ('Informações Básicas', {
                'fields': ('nome', 'vereador', 'setor')
            }),
            ('Contato', {
                'fields': ('telefone', 'email')
            }),
            ('Informações do Sistema', {
                'fields': ('data_criacao', 'data_atualizacao'),
                'classes': ('collapse',)
            }),
        )
    
    # Registrando o modelo Gabinete no admin
    admin.site.register(Gabinete, GabineteAdmin)
    
except ImportError:
    # Em caso de erro de importação, não registra o modelo
    pass
