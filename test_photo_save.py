#!/usr/bin/env python
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
django.setup()

from apps.recepcao.models import Visitante
from django.core.files import File
from apps.recepcao.utils.image_utils import process_image
import tempfile

def test_photo_save():
    """Testa o salvamento de fotos em visitantes"""
    print("Testando salvamento de fotos...")
    
    # Buscar um visitante para teste
    visitante = Visitante.objects.first()
    if not visitante:
        print("Nenhum visitante encontrado para teste")
        return
    
    print(f"Testando com visitante: {visitante.nome_completo} (ID: {visitante.id})")
    
    # Verificar estado atual
    print(f"Estado atual:")
    print(f"  Foto original: {visitante.foto}")
    print(f"  Foto thumbnail: {visitante.foto_thumbnail}")
    print(f"  Foto medium: {visitante.foto_medium}")
    print(f"  Foto large: {visitante.foto_large}")
    
    # Criar uma imagem de teste
    try:
        from PIL import Image
        import io
        
        # Criar uma imagem simples
        img = Image.new('RGB', (100, 100), color='red')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(img_buffer.getvalue())
            temp_file_path = temp_file.name
        
        print(f"Imagem de teste criada: {temp_file_path}")
        
        # Testar processamento de imagem
        with open(temp_file_path, 'rb') as f:
            from django.core.files.uploadedfile import SimpleUploadedFile
            test_file = SimpleUploadedFile(
                'test_photo.jpg',
                f.read(),
                content_type='image/jpeg'
            )
            
            print("Processando imagem...")
            processed_images = process_image(test_file)
            print(f"Imagens processadas: {list(processed_images.keys())}")
            
            # Testar salvamento
            print("Salvando fotos...")
            visitante.foto = test_file
            
            # Salvar versões processadas
            if 'thumbnail' in processed_images:
                visitante.foto_thumbnail.save(
                    processed_images['thumbnail'].name,
                    processed_images['thumbnail'],
                    save=False
                )
                print("  ✓ Thumbnail salvo")
            
            if 'medium' in processed_images:
                visitante.foto_medium.save(
                    processed_images['medium'].name,
                    processed_images['medium'],
                    save=False
                )
                print("  ✓ Medium salvo")
            
            if 'large' in processed_images:
                visitante.foto_large.save(
                    processed_images['large'].name,
                    processed_images['large'],
                    save=False
                )
                print("  ✓ Large salvo")
            
            # Salvar o visitante
            visitante.save()
            print("  ✓ Visitante salvo")
            
            # Verificar estado após salvamento
            print(f"Estado após salvamento:")
            print(f"  Foto original: {visitante.foto}")
            print(f"  Foto thumbnail: {visitante.foto_thumbnail}")
            print(f"  Foto medium: {visitante.foto_medium}")
            print(f"  Foto large: {visitante.foto_large}")
            
            # Verificar se os arquivos existem
            if visitante.foto and os.path.exists(visitante.foto.path):
                print(f"  ✓ Arquivo original existe: {visitante.foto.path}")
            else:
                print(f"  ✗ Arquivo original não existe")
            
            for size in ['thumbnail', 'medium', 'large']:
                foto_field = getattr(visitante, f'foto_{size}')
                if foto_field and os.path.exists(foto_field.path):
                    print(f"  ✓ Arquivo {size} existe: {foto_field.path}")
                else:
                    print(f"  ✗ Arquivo {size} não existe")
        
        # Limpar arquivo temporário
        os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_photo_save() 