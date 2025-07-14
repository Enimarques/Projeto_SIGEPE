#!/usr/bin/env python
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Buscar o usuário admin
    user = User.objects.get(username='admin')
    # Definir a senha
    user.set_password('admin123')
    user.save()
    print('Senha do superusuário admin definida com sucesso!')
    print('Usuário: admin')
    print('Senha: admin123')
except User.DoesNotExist:
    print('Usuário admin não encontrado. Criando...')
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário admin criado com sucesso!')
    print('Usuário: admin')
    print('Senha: admin123')
except Exception as e:
    print(f'Erro: {e}') 