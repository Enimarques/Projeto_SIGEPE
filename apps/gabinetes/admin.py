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
                'fields': ('nome', 'vereador', 'setor'),
                'description': 'Preencha os dados principais do gabinete.'
            }),
            ('Contato', {
                'fields': ('telefone', 'email')
            }),
            ('Informações do Sistema', {
                'fields': ('data_criacao', 'data_atualizacao'),
                'classes': ('collapse',)
            }),
        )
        
        def formfield_for_dbfield(self, db_field, **kwargs):
            field = super().formfield_for_dbfield(db_field, **kwargs)
            if db_field.name == "nome":
                field.help_text = "Informe o nome completo do(a) vereador(a)"
            elif db_field.name == "vereador":
                field.help_text = "Nome de uso público, como ele(a) é mais conhecido(a) pela população"
            return field
    
    # Registrando o modelo Gabinete no admin
    admin.site.register(Gabinete, GabineteAdmin)
    
except ImportError:
    # Em caso de erro de importação, não registra o modelo
    pass
