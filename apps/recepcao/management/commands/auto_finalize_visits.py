import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.recepcao.models import Visita


class Command(BaseCommand):
    help = (
        "Finaliza automaticamente visitas em andamento há mais de 24 horas. "
        "Use --force-all para finalizar todas as visitas em aberto, independentemente do tempo."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-all",
            action="store_true",
            help="Finaliza todas as visitas em andamento, ignorando a janela de 24h.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra o que seria feito sem aplicar mudanças.",
        )

    def handle(self, *args, **options):
        logger = logging.getLogger("django.server")

        now = timezone.now()
        cutoff = now - timedelta(hours=24)

        base_qs = Visita.objects.filter(status="em_andamento")
        if options["force_all"]:
            target_qs = base_qs
        else:
            target_qs = base_qs.filter(data_entrada__lte=cutoff)

        total_open = base_qs.count()
        total_target = target_qs.count()

        if options["dry_run"]:
            msg = (
                f"[auto_finalize_visits] DRY-RUN: abertas={total_open}, a_finalizar={total_target}, "
                f"force_all={options['force_all']}"
            )
            self.stdout.write(self.style.WARNING(msg))
            logger.info(msg)
            return

        updated = 0
        if total_target > 0:
            updated = target_qs.update(status="finalizada", data_saida=now)

        msg = (
            f"[auto_finalize_visits] Concluído: abertas={total_open}, finalizadas={updated}, "
            f"force_all={options['force_all']}"
        )
        self.stdout.write(self.style.SUCCESS(msg))
        logger.info(msg)


