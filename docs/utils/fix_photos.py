#!/usr/bin/env python
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
django.setup()

from apps.recepcao.models import Visitante
from django.core.cache import cache
from django.core.files import File
from PIL import Image
import io

def check_and_fix_photos():
    """Verifica e corrige problemas com as fotos dos visitantes"""
    print("Verificando e corrigindo fotos dos visitantes...")
    
    visitantes = Visitante.objects.all()
    for visitante in visitantes:
        print(f"\nVisitante: {visitante.nome_completo} (ID: {visitante.id})")
        
        # Verificar se tem foto original
        if visitante.foto:
            if os.path.exists(visitante.foto.path):
                print(f"  ✓ Foto original existe: {visitante.foto.path}")
                
                # Verificar se as fotos processadas existem
                missing_sizes = []
                for size in ['thumbnail', 'medium', 'large']:
                    foto_field = getattr(visitante, f'foto_{size}')
                    if not foto_field or not os.path.exists(foto_field.path):
                        missing_sizes.append(size)
                        print(f"  ✗ Foto {size} não existe")
                    else:
                        print(f"  ✓ Foto {size} existe")
                
                # Se faltam fotos processadas, recriar
                if missing_sizes:
                    print(f"  Recriando fotos processadas: {missing_sizes}")
                    try:
                        from apps.recepcao.utils.image_utils import process_image
                        
                        # Processar a imagem novamente
                        processed_images = process_image(visitante.foto)
                        
                        # Salvar as versões processadas
                        for size in missing_sizes:
                            if size in processed_images:
                                img_file = processed_images[size]
                                setattr(visitante, f'foto_{size}', img_file)
                                print(f"    ✓ Foto {size} recriada")
                        
                        visitante.save()
                        print(f"    ✓ Visitante salvo com sucesso")
                        
                    except Exception as e:
                        print(f"    ✗ Erro ao recriar fotos: {str(e)}")
            else:
                print(f"  ✗ Foto original não encontrada: {visitante.foto.path}")
                # Limpar referências de fotos inexistentes
                visitante.foto = None
                visitante.foto_thumbnail = None
                visitante.foto_medium = None
                visitante.foto_large = None
                visitante.save()
                print(f"    ✓ Referências de fotos limpas")
        else:
            print("  - Sem foto original")
        
        # Limpar cache
        for size in ['thumbnail', 'medium', 'large']:
            cache_key = f'visitante_foto_{visitante.id}_{size}'
            cache.delete(cache_key)

def test_photo_urls():
    """Testa as URLs das fotos após as correções"""
    print("\n" + "="*50)
    print("Testando URLs das fotos...")
    
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
    check_and_fix_photos()
    test_photo_urls()
    print("\nProcesso concluído!") 