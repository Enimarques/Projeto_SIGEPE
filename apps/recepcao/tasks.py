import logging
import time
from datetime import timedelta

from django.utils import timezone
from django.core.management import call_command

from apps.recepcao.models import Visita


def auto_finalize_visits(force_all: bool = False) -> int:
    """
    Finaliza visitas em andamento. Por padrão, apenas as com mais de 24h.
    Se force_all=True, finaliza todas as em andamento.

    Retorna a quantidade de visitas finalizadas.
    """
    logger = logging.getLogger("django.server")

    now = timezone.now()
    cutoff = now - timedelta(hours=24)

    base_qs = Visita.objects.filter(status="em_andamento")
    target_qs = base_qs if force_all else base_qs.filter(data_entrada__lte=cutoff)

    total_open = base_qs.count()
    total_target = target_qs.count()

    if total_target == 0:
        logger.info(
            f"[scheduler auto_finalize_visits] Nada a finalizar: abertas={total_open}, alvo={total_target}, force_all={force_all}"
        )
        return 0

    updated = target_qs.update(status="finalizada", data_saida=now)
    logger.info(
        f"[scheduler auto_finalize_visits] Finalizadas: {updated} (abertas={total_open}, alvo={total_target}, force_all={force_all})"
    )
    return updated


def limpar_arquivados():
    """
    Remove definitivamente visitantes e visitas arquivados há mais de 6 meses.
    Retorna a quantidade de registros removidos.
    """
    logger = logging.getLogger("django.server")
    try:
        # Chama o management command de limpeza
        from io import StringIO
        out = StringIO()
        call_command('limpar_arquivados', stdout=out)
        output = out.getvalue()
        logger.info(f"[scheduler limpar_arquivados] {output}")
        return True
    except Exception as exc:
        logger.exception(f"[scheduler] Falha ao executar limpar_arquivados: {exc}")
        return False


def run_daily_at(hour: int = 2, minute: int = 0, second: int = 0, force_all: bool = False):
    """
    Loop simples que dorme até a próxima execução diária e roda as tarefas.
    """
    logger = logging.getLogger("django.server")
    while True:
        now = timezone.localtime()
        next_run = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        if now >= next_run:
            next_run += timedelta(days=1)

        sleep_seconds = (next_run - now).total_seconds()
        logger.info(
            f"[scheduler] Próxima execução de tarefas diárias às {next_run.isoformat()} (em {int(sleep_seconds)}s)"
        )
        time.sleep(max(1, int(sleep_seconds)))

        try:
            # Executa finalização de visitas
            auto_finalize_visits(force_all=force_all)
            # Executa limpeza de arquivados
            limpar_arquivados()
        except Exception as exc:
            logger.exception(f"[scheduler] Falha ao executar tarefas diárias: {exc}")


