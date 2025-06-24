from django.apps import AppConfig

class RecepcaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recepcao'
    verbose_name = 'Recepção'

    def ready(self):
        # Importa os signals para que eles sejam registrados
        import apps.recepcao.signals
