from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import os
import re
import shutil
import logging
from apps.recepcao.models import Visitante

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Identifica e corrige fotos órfãs na pasta media/fotos_visitantes/'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa em modo de teste sem fazer alterações',
        )
        parser.add_argument(
            '--backup-only',
            action='store_true',
            help='Apenas move fotos órfãs para backup sem tentar corrigir',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        backup_only = options['backup_only']
        
        self.stdout.write(
            self.style.SUCCESS('Iniciando limpeza de fotos órfãs...')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('MODO DE TESTE - Nenhuma alteração será feita')
            )
        
        # Executa a limpeza
        self.cleanup_orphan_photos(dry_run, backup_only)
        
        self.stdout.write(
            self.style.SUCCESS('Limpeza concluída!')
        )

    def find_orphan_photos(self):
        """Encontra fotos órfãs na pasta fotos_visitantes"""
        photos_dir = Path(settings.MEDIA_ROOT) / 'fotos_visitantes'
        orphan_photos = []
        
        if not photos_dir.exists():
            self.stdout.write(
                self.style.WARNING("Pasta fotos_visitantes não encontrada")
            )
            return orphan_photos
        
        # Procura por arquivos .jpg na raiz da pasta
        for file_path in photos_dir.glob('*.jpg'):
            if file_path.is_file():
                orphan_photos.append(file_path)
                self.stdout.write(f"Foto órfã encontrada: {file_path.name}")
        
        return orphan_photos

    def find_visitante_by_photo_field(self, photo_path):
        """Tenta encontrar o visitante pelo campo de foto"""
        photo_filename = photo_path.name
        
        # Procura nos campos de foto do modelo Visitante
        for field_name in ['foto', 'foto_large', 'foto_medium', 'foto_thumbnail']:
            try:
                # Filtra visitantes que têm este arquivo no campo
                visitantes = Visitante.objects.filter(**{f"{field_name}__endswith": photo_filename})
                if visitantes.exists():
                    return visitantes.first(), field_name
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Erro ao buscar por {field_name}: {e}")
                )
        
        return None, None

    def move_photo_to_correct_folder(self, photo_path, visitante, dry_run=False):
        """Move a foto para a pasta correta do visitante"""
        try:
            # Gera o caminho correto usando a função do modelo
            from apps.recepcao.models import get_visitor_upload_path
            
            # Cria uma instância temporária para usar a função
            temp_instance = Visitante()
            temp_instance.id = visitante.id
            temp_instance.nome_completo = visitante.nome_completo
            temp_instance.data_nascimento = visitante.data_nascimento
            
            correct_path = get_visitor_upload_path(temp_instance, photo_path.name)
            full_correct_path = Path(settings.MEDIA_ROOT) / correct_path
            
            if dry_run:
                self.stdout.write(f"DRY RUN: Moveria {photo_path.name} -> {correct_path}")
                return True
            
            # Cria a pasta de destino se não existir
            full_correct_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move o arquivo
            shutil.move(str(photo_path), str(full_correct_path))
            self.stdout.write(
                self.style.SUCCESS(f"Foto movida: {photo_path.name} -> {correct_path}")
            )
            
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao mover foto {photo_path.name}: {e}")
            )
            return False

    def update_visitante_photo_field(self, visitante, photo_filename, field_name, dry_run=False):
        """Atualiza o campo de foto do visitante"""
        try:
            # Gera o caminho correto
            from apps.recepcao.models import get_visitor_upload_path
            
            temp_instance = Visitante()
            temp_instance.id = visitante.id
            temp_instance.nome_completo = visitante.nome_completo
            temp_instance.data_nascimento = visitante.data_nascimento
            
            correct_path = get_visitor_upload_path(temp_instance, photo_filename)
            
            if dry_run:
                self.stdout.write(f"DRY RUN: Atualizaria campo {field_name} do visitante {visitante.id}")
                return True
            
            # Atualiza o campo
            setattr(visitante, field_name, correct_path)
            visitante.save(update_fields=[field_name])
            
            self.stdout.write(
                self.style.SUCCESS(f"Campo {field_name} atualizado para visitante {visitante.id}")
            )
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao atualizar campo {field_name} do visitante {visitante.id}: {e}")
            )
            return False

    def cleanup_orphan_photos(self, dry_run=False, backup_only=False):
        """Limpa fotos órfãs que não podem ser vinculadas"""
        photos_dir = Path(settings.MEDIA_ROOT) / 'fotos_visitantes'
        backup_dir = photos_dir / 'backup_orphans'
        
        # Cria pasta de backup se não for dry_run
        if not dry_run:
            backup_dir.mkdir(exist_ok=True)
        
        orphan_photos = self.find_orphan_photos()
        processed_count = 0
        moved_count = 0
        backup_count = 0
        
        if not orphan_photos:
            self.stdout.write(
                self.style.SUCCESS("Nenhuma foto órfã encontrada!")
            )
            return
        
        for photo_path in orphan_photos:
            processed_count += 1
            self.stdout.write(f"Processando foto {processed_count}/{len(orphan_photos)}: {photo_path.name}")
            
            if backup_only:
                # Apenas move para backup
                if not dry_run:
                    backup_path = backup_dir / photo_path.name
                    shutil.move(str(photo_path), str(backup_path))
                    backup_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Foto {photo_path.name} movida para backup")
                    )
                else:
                    self.stdout.write(f"DRY RUN: Moveria {photo_path.name} para backup")
                    backup_count += 1
                continue
            
            # Tenta encontrar o visitante
            visitante, field_name = self.find_visitante_by_photo_field(photo_path)
            
            if visitante and field_name:
                # Move para pasta correta
                if self.move_photo_to_correct_folder(photo_path, visitante, dry_run):
                    # Atualiza o campo do visitante
                    if self.update_visitante_photo_field(visitante, photo_path.name, field_name, dry_run):
                        moved_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Foto {photo_path.name} processada com sucesso")
                        )
                    else:
                        # Se não conseguiu atualizar, faz backup
                        if not dry_run:
                            backup_path = backup_dir / photo_path.name
                            shutil.move(str(photo_path), str(backup_path))
                            backup_count += 1
                            self.stdout.write(
                                self.style.WARNING(f"Foto {photo_path.name} movida para backup")
                            )
                        else:
                            self.stdout.write(f"DRY RUN: Moveria {photo_path.name} para backup")
                            backup_count += 1
                else:
                    # Se não conseguiu mover, faz backup
                    if not dry_run:
                        backup_path = backup_dir / photo_path.name
                        shutil.move(str(photo_path), str(backup_path))
                        backup_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"Foto {photo_path.name} movida para backup")
                        )
                    else:
                        self.stdout.write(f"DRY RUN: Moveria {photo_path.name} para backup")
                        backup_count += 1
            else:
                # Foto não pode ser vinculada, faz backup
                if not dry_run:
                    backup_path = backup_dir / photo_path.name
                    shutil.move(str(photo_path), str(backup_path))
                    backup_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Foto órfã {photo_path.name} movida para backup")
                    )
                else:
                    self.stdout.write(f"DRY RUN: Moveria {photo_path.name} para backup")
                    backup_count += 1
        
        # Relatório final
        self.stdout.write(
            self.style.SUCCESS(f"\nProcessamento concluído:")
        )
        self.stdout.write(f"- Total processado: {processed_count}")
        self.stdout.write(f"- Movidas com sucesso: {moved_count}")
        self.stdout.write(f"- Movidas para backup: {backup_count}")
        
        if backup_count > 0 and not dry_run:
            self.stdout.write(
                self.style.WARNING(f"Fotos em backup: {backup_dir}")
            )
