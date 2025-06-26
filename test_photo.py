#!/usr/bin/env python
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
django.setup()

from apps.recepcao.models import Visitante

def test_photos():
    """Testa o carregamento de fotos dos visitantes"""
    print("Testando fotos dos visitantes...")
    
    visitantes = Visitante.objects.all()
    for visitante in visitantes:
        print(f"\nVisitante: {visitante.nome_completo} (ID: {visitante.id})")
        
        # Verificar foto original
        if visitante.foto:
            print(f"  Foto original: {visitante.foto.url}")
            if os.path.exists(visitante.foto.path):
                print(f"    ✓ Arquivo existe: {visitante.foto.path}")
            else:
                print(f"    ✗ Arquivo não existe: {visitante.foto.path}")
        else:
            print("  Sem foto original")
        
        # Verificar fotos processadas
        for size in ['thumbnail', 'medium', 'large']:
            foto_field = getattr(visitante, f'foto_{size}')
            if foto_field:
                print(f"  Foto {size}: {foto_field.url}")
                if os.path.exists(foto_field.path):
                    print(f"    ✓ Arquivo existe: {foto_field.path}")
                else:
                    print(f"    ✗ Arquivo não existe: {foto_field.path}")
            else:
                print(f"  Sem foto {size}")

if __name__ == '__main__':
    test_photos() 