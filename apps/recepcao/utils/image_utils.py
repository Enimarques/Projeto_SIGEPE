from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import magic
import uuid

def process_image(image_file, max_size_mb=5):
    """
    Process and validate an uploaded image.
    - Validates file type and size
    - Compresses the image
    - Creates different sizes
    - Returns a dict with processed images
    """
    # Validar tamanho máximo (5MB por padrão)
    if image_file.size > max_size_mb * 1024 * 1024:
        raise ValueError(f'O arquivo é muito grande. Tamanho máximo permitido: {max_size_mb}MB')

    # Abrir imagem com PIL
    try:
        img = Image.open(image_file)
    except Exception:
        raise ValueError('Arquivo de imagem inválido ou corrompido.')

    # Converter para RGB se necessário
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Gerar nome de arquivo único
    filename = str(uuid.uuid4())
    
    # Criar diferentes tamanhos
    sizes = {
        'thumbnail': (100, 100),
        'medium': (300, 300),
        'large': (800, 800)
    }
    
    processed_images = {}
    
    for size_name, dimensions in sizes.items():
        # Criar cópia da imagem
        img_copy = img.copy()
        
        # Redimensionar mantendo proporção
        img_copy.thumbnail(dimensions, Image.Resampling.LANCZOS)
        
        # Salvar em buffer com compressão
        output = BytesIO()
        
        # Usar qualidade diferente para cada tamanho
        quality = 85 if size_name == 'large' else 75
        
        img_copy.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # Criar arquivo para Django
        processed_images[size_name] = InMemoryUploadedFile(
            output,
            'ImageField',
            f"{filename}_{size_name}.jpg",
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
    
    return processed_images

def sanitize_filename(filename):
    """
    Sanitiza o nome do arquivo para evitar problemas de segurança.
    """
    # Remove caracteres especiais e espaços
    filename = "".join(c for c in filename if c.isalnum() or c in '._-')
    
    # Adiciona UUID para garantir unicidade
    name, ext = os.path.splitext(filename)
    return f"{name}_{str(uuid.uuid4())[:8]}{ext}" 