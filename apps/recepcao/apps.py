from django.apps import AppConfig

class RecepcaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recepcao'
    verbose_name = 'Recepção'

    def ready(self):
        # Importa os signals para que eles sejam registrados
        import apps.recepcao.signals

        # Inicia o agendador diário às 02:00 (thread daemon) apenas em processos web/worker
        # Evita rodar durante migrações, shell e comandos de coleta estática
        import os
        import threading
        import sys

        # Previne múltiplas threads em recarregamento automático (runserver)
        if os.environ.get('RUN_MAIN') == 'true':
            return

        disallowed_cmds = {'makemigrations', 'migrate', 'collectstatic', 'shell', 'test'}
        if any(cmd in sys.argv for cmd in disallowed_cmds):
            return

        try:
            from apps.recepcao.tasks import run_daily_at

            thread = threading.Thread(target=run_daily_at, kwargs={'hour': 2, 'minute': 0, 'second': 0, 'force_all': True})
            thread.daemon = True
            thread.start()
        except Exception:
            # Em caso de falha, não impede o start do Django
            import logging
            logging.getLogger('django.server').exception('[scheduler] Falha ao iniciar thread do agendador diário')