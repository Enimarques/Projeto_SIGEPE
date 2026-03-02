import logging
from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.recepcao.models import VisitanteArquivado


class Command(BaseCommand):
    help = (
        "Verifica e lista visitantes arquivados duplicados (mesmo id_original). "
        "Use --remover para remover duplicatas, mantendo apenas o mais antigo."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--remover",
            action="store_true",
            help="Remove duplicatas, mantendo apenas o registro mais antigo de cada id_original.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra o que seria feito sem aplicar mudanças.",
        )

    def handle(self, *args, **options):
        logger = logging.getLogger("django.server")

        # Encontrar duplicatas agrupando por id_original
        duplicatas = (
            VisitanteArquivado.objects.values("id_original")
            .annotate(count=Count("id_original"))
            .filter(count__gt=1)
        )

        total_duplicatas = duplicatas.count()

        if total_duplicatas == 0:
            msg = "[verificar_duplicatas_arquivados] Nenhuma duplicata encontrada."
            self.stdout.write(self.style.SUCCESS(msg))
            logger.info(msg)
            return

        msg = f"[verificar_duplicatas_arquivados] Encontradas {total_duplicatas} duplicata(s)."
        self.stdout.write(self.style.WARNING(msg))
        logger.info(msg)

        removidos = 0
        for dup in duplicatas:
            id_original = dup["id_original"]
            registros = VisitanteArquivado.objects.filter(
                id_original=id_original
            ).order_by("data_arquivamento")

            # O primeiro é o mais antigo (manter)
            manter = registros.first()
            remover = registros[1:]  # Todos os outros são duplicatas

            self.stdout.write(
                f"\nID Original: {id_original} - {manter.nome_completo}"
            )
            self.stdout.write(f"  Manter: ID {manter.id} (arquivado em {manter.data_arquivamento})")
            
            for reg in remover:
                self.stdout.write(
                    f"  {'[DRY-RUN] ' if options['dry_run'] else ''}Remover: ID {reg.id} "
                    f"(arquivado em {reg.data_arquivamento})"
                )

                if not options["dry_run"] and options["remover"]:
                    try:
                        # Deletar visitas arquivadas relacionadas primeiro
                        reg.visitas_arquivadas.all().delete()
                        # Deletar o registro duplicado
                        reg.delete()
                        removidos += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"    ✓ Removido com sucesso")
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"    ✗ Erro ao remover: {e}")
                        )
                        logger.error(f"Erro ao remover duplicata ID {reg.id}: {e}")

        if options["dry_run"]:
            msg = (
                f"[verificar_duplicatas_arquivados] DRY-RUN: "
                f"{total_duplicatas} duplicata(s) encontrada(s), "
                f"{sum(len(VisitanteArquivado.objects.filter(id_original=d['id_original'])) - 1 for d in duplicatas)} "
                f"registro(s) seriam removido(s)."
            )
        elif options["remover"]:
            msg = (
                f"[verificar_duplicatas_arquivados] Concluído: "
                f"{removidos} registro(s) duplicado(s) removido(s)."
            )
        else:
            msg = (
                f"[verificar_duplicatas_arquivados] Use --remover para remover as duplicatas."
            )

        self.stdout.write(self.style.SUCCESS(f"\n{msg}"))
        logger.info(msg)

