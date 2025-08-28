#!/usr/bin/env python
"""
Script para identificar e corrigir fotos órfãs na pasta media/fotos_visitantes/

Este script:
1. Identifica fotos que estão na raiz da pasta (não em subpastas)
2. Tenta vincular essas fotos aos visitantes corretos
3. Move as fotos para as pastas corretas
4. Limpa fotos órfãs que não podem ser vinculadas

Uso: python manage.py shell < fix_orphan_photos.py
"""

import os
import re
import shutil
from pathlib import Path
from django.conf import settings
from apps.recepcao.models import Visitante
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_uuid_from_filename(filename):
    """Extrai UUID do nome do arquivo"""
    # Padrão: UUID_tamanho.jpg
    pattern = r'^([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})_(large|medium|thumbnail)\.jpg$'
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return None

def find_orphan_photos():
    """Encontra fotos órfãs na pasta fotos_visitantes"""
    photos_dir = Path(settings.MEDIA_ROOT) / 'fotos_visitantes'
    orphan_photos = []
    
    if not photos_dir.exists():
        logger.warning("Pasta fotos_visitantes não encontrada")
        return orphan_photos
    
    # Procura por arquivos .jpg na raiz da pasta
    for file_path in photos_dir.glob('*.jpg'):
        if file_path.is_file():
            orphan_photos.append(file_path)
            logger.info(f"Foto órfã encontrada: {file_path.name}")
    
    return orphan_photos

def find_visitante_by_photo_field(photo_path):
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
            logger.error(f"Erro ao buscar por {field_name}: {e}")
    
    return None, None

def move_photo_to_correct_folder(photo_path, visitante):
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
        
        # Cria a pasta de destino se não existir
        full_correct_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move o arquivo
        shutil.move(str(photo_path), str(full_correct_path))
        logger.info(f"Foto movida: {photo_path.name} -> {correct_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao mover foto {photo_path.name}: {e}")
        return False

def update_visitante_photo_field(visitante, photo_filename, field_name):
    """Atualiza o campo de foto do visitante"""
    try:
        # Gera o caminho correto
        from apps.recepcao.models import get_visitor_upload_path
        
        temp_instance = Visitante()
        temp_instance.id = visitante.id
        temp_instance.nome_completo = visitante.nome_completo
        temp_instance.data_nascimento = visitante.data_nascimento
        
        correct_path = get_visitor_upload_path(temp_instance, photo_filename)
        
        # Atualiza o campo
        setattr(visitante, field_name, correct_path)
        visitante.save(update_fields=[field_name])
        
        logger.info(f"Campo {field_name} atualizado para visitante {visitante.id}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao atualizar campo {field_name} do visitante {visitante.id}: {e}")
        return False

def cleanup_orphan_photos():
    """Limpa fotos órfãs que não podem ser vinculadas"""
    photos_dir = Path(settings.MEDIA_ROOT) / 'fotos_visitantes'
    backup_dir = photos_dir / 'backup_orphans'
    
    # Cria pasta de backup
    backup_dir.mkdir(exist_ok=True)
    
    orphan_photos = find_orphan_photos()
    processed_count = 0
    moved_count = 0
    backup_count = 0
    
    for photo_path in orphan_photos:
        processed_count += 1
        logger.info(f"Processando foto {processed_count}/{len(orphan_photos)}: {photo_path.name}")
        
        # Tenta encontrar o visitante
        visitante, field_name = find_visitante_by_photo_field(photo_path)
        
        if visitante and field_name:
            # Move para pasta correta
            if move_photo_to_correct_folder(photo_path, visitante):
                # Atualiza o campo do visitante
                if update_visitante_photo_field(visitante, photo_path.name, field_name):
                    moved_count += 1
                    logger.info(f"Foto {photo_path.name} processada com sucesso")
                else:
                    # Se não conseguiu atualizar, faz backup
                    backup_path = backup_dir / photo_path.name
                    shutil.move(str(photo_path), str(backup_path))
                    backup_count += 1
                    logger.warning(f"Foto {photo_path.name} movida para backup")
            else:
                # Se não conseguiu mover, faz backup
                backup_path = backup_dir / photo_path.name
                shutil.move(str(photo_path), str(backup_path))
                backup_count += 1
                logger.warning(f"Foto {photo_path.name} movida para backup")
        else:
            # Foto não pode ser vinculada, faz backup
            backup_path = backup_dir / photo_path.name
            shutil.move(str(photo_path), str(backup_path))
            backup_count += 1
            logger.warning(f"Foto órfã {photo_path.name} movida para backup")
    
    logger.info(f"Processamento concluído:")
    logger.info(f"- Total processado: {processed_count}")
    logger.info(f"- Movidas com sucesso: {moved_count}")
    logger.info(f"- Movidas para backup: {backup_count}")
    
    if backup_count > 0:
        logger.info(f"Fotos em backup: {backup_dir}")

def main():
    """Função principal"""
    logger.info("Iniciando limpeza de fotos órfãs...")
    
    # Verifica se estamos no ambiente Django
    try:
        from django.conf import settings
        if not settings.configured:
            logger.error("Django não está configurado. Execute este script dentro do shell do Django.")
            return
    except ImportError:
        logger.error("Django não está disponível. Execute este script dentro do shell do Django.")
        return
    
    # Executa a limpeza
    cleanup_orphan_photos()
    
    logger.info("Limpeza concluída!")

if __name__ == "__main__":
    main()
