import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.recepcao.models import VisitanteArquivado, VisitaArquivada


class Command(BaseCommand):
    help = (
        "Remove definitivamente visitantes e visitas arquivados há mais de 6 meses. "
        "Use --dry-run para ver o que seria removido sem aplicar mudanças."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra o que seria removido sem aplicar mudanças.",
        )
        parser.add_argument(
            "--force-all",
            action="store_true",
            help="Remove todos os arquivados, independentemente do tempo.",
        )

    def handle(self, *args, **options):
        logger = logging.getLogger("django.server")

        now = timezone.now()
        cutoff = now - timedelta(days=180)  # 6 meses

        base_qs = VisitanteArquivado.objects.all()
        if options["force_all"]:
            target_qs = base_qs
        else:
            target_qs = base_qs.filter(data_arquivamento__lte=cutoff)

        total_arquivados = base_qs.count()
        total_para_remover = target_qs.count()

        if options["dry_run"]:
            msg = (
                f"[limpar_arquivados] DRY-RUN: total_arquivados={total_arquivados}, "
                f"a_remover={total_para_remover}, "
                f"cutoff={cutoff.date()}, force_all={options['force_all']}"
            )
            self.stdout.write(self.style.WARNING(msg))
            logger.info(msg)
            
            # Mostrar alguns exemplos
            if total_para_remover > 0:
                self.stdout.write("\nExemplos de registros que seriam removidos:")
                for visitante in target_qs[:5]:
                    self.stdout.write(
                        f"  - {visitante.nome_completo} (arquivado em {visitante.data_arquivamento.date()})"
                    )
                if total_para_remover > 5:
                    self.stdout.write(f"  ... e mais {total_para_remover - 5} registro(s)")
            return

        removed_count = 0
        visitas_removidas = 0
        
        if total_para_remover > 0:
            for visitante_arquivado in target_qs:
                try:
                    # Contar visitas antes de remover
                    num_visitas = visitante_arquivado.visitas_arquivadas.count()
                    visitas_removidas += num_visitas
                    
                    # Marcar data de exclusão definitiva antes de deletar
                    visitante_arquivado.data_exclusao_definitiva = now
                    visitante_arquivado.save()
                    
                    # Deletar o visitante arquivado (cascade deleta as visitas)
                    visitante_arquivado.delete()
                    removed_count += 1
                    
                except Exception as e:
                    logger.error(
                        f"Erro ao remover visitante arquivado {visitante_arquivado.id}: {e}",
                        exc_info=True
                    )
                    self.stdout.write(
                        self.style.ERROR(
                            f"Erro ao remover {visitante_arquivado.nome_completo}: {e}"
                        )
                    )

        msg = (
            f"[limpar_arquivados] Concluído: total_arquivados={total_arquivados}, "
            f"removidos={removed_count}, visitas_removidas={visitas_removidas}, "
            f"cutoff={cutoff.date()}, force_all={options['force_all']}"
        )
        self.stdout.write(self.style.SUCCESS(msg))
        logger.info(msg)

