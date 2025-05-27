from django.contrib import admin
from django.apps import apps

# Registrar explicitamente os modelos do app de veículos
from apps.veiculos.models import Veiculo

# Registrar o modelo Veiculo com uma classe de administração personalizada
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'modelo', 'cor', 'visitante')
    search_fields = ('placa', 'modelo', 'visitante__nome')
    list_filter = ('tipo', 'cor')

# Registrar os modelos no admin
admin.site.register(Veiculo, VeiculoAdmin)

# Registrar automaticamente todos os modelos que ainda não foram registrados
for app_config in apps.get_app_configs():
    app = app_config.name.split('.')[-1]
    
    # Pular apps do Django e apps que já têm seus próprios registros
    if app in ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
        continue
    
    for model in app_config.get_models():
        try:
            # Verificar se o modelo já está registrado
            if model not in admin.site._registry:
                admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
