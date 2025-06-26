#!/usr/bin/env python
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
django.setup()

from django.core.cache import cache
from apps.recepcao.models import Visitante

def clear_photo_cache():
    """Limpa o cache de fotos dos visitantes"""
    print("Limpando cache de fotos...")
    
    # Limpar cache para todos os visitantes
    visitantes = Visitante.objects.all()
    for visitante in visitantes:
        for size in ['thumbnail', 'medium', 'large']:
            cache_key = f'visitante_foto_{visitante.id}_{size}'
            cache.delete(cache_key)
            print(f"Cache limpo para visitante {visitante.id}, tamanho {size}")
    
    print("Cache de fotos limpo com sucesso!")

def check_photo_files():
    """Verifica se os arquivos de foto existem"""
    print("\nVerificando arquivos de foto...")
    
    visitantes = Visitante.objects.all()
    for visitante in visitantes:
        print(f"\nVisitante: {visitante.nome_completo} (ID: {visitante.id})")
        
        # Verificar foto original
        if visitante.foto:
            if os.path.exists(visitante.foto.path):
                print(f"  ✓ Foto original: {visitante.foto.path}")
            else:
                print(f"  ✗ Foto original não encontrada: {visitante.foto.path}")
        else:
            print("  - Sem foto original")
        
        # Verificar fotos processadas
        for size in ['thumbnail', 'medium', 'large']:
            foto_field = getattr(visitante, f'foto_{size}')
            if foto_field:
                if os.path.exists(foto_field.path):
                    print(f"  ✓ Foto {size}: {foto_field.path}")
                else:
                    print(f"  ✗ Foto {size} não encontrada: {foto_field.path}")
            else:
                print(f"  - Sem foto {size}")

def test_photo_urls():
    """Testa as URLs das fotos"""
    print("\nTestando URLs das fotos...")
    
    visitantes = Visitante.objects.all()
    for visitante in visitantes:
        print(f"\nVisitante: {visitante.nome_completo} (ID: {visitante.id})")
        
        # Testar get_foto_url
        for size in ['thumbnail', 'medium', 'large']:
            url = visitante.get_foto_url(size)
            if url:
                print(f"  ✓ URL {size}: {url}")
            else:
                print(f"  ✗ URL {size}: None")

if __name__ == '__main__':
    clear_photo_cache()
    check_photo_files()
    test_photo_urls() 