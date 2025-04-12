# Script para verificar configurações de modelos
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIGEPE.settings')
application = get_wsgi_application()

from apps.recepcao.models import Visita, Visitante

# Verificar a configuração on_delete na relação
visita_visitante_field = Visita._meta.get_field('visitante')
print(f"Campo 'visitante' em Visita:")
print(f"- Tipo: {type(visita_visitante_field)}")
print(f"- on_delete: {visita_visitante_field.remote_field.on_delete}")
print(f"- Relacionado com: {visita_visitante_field.related_model}")
print("\n")

# Verificar as relações de um visitante específico
try:
    visitante_id = 5  # O ID que você está tentando excluir
    visitante = Visitante.objects.get(id=visitante_id)
    print(f"Encontrado Visitante: {visitante.nome_completo} (ID: {visitante_id})")
    
    # Verificar visitas relacionadas
    visitas = Visita.objects.filter(visitante=visitante)
    print(f"Visitas relacionadas: {visitas.count()}")
    
    for i, visita in enumerate(visitas, 1):
        print(f"{i}. Visita ID: {visita.id}, Data: {visita.data_entrada}")
    
    print("\nCom esta configuração, é necessário excluir as visitas antes do visitante.")
    print("Deseja excluir o visitante e suas visitas? (sim/não)")
    resposta = input()
    
    if resposta.lower() in ['sim', 's', 'yes', 'y']:
        print(f"Excluindo {visitas.count()} visitas...")
        visitas.delete()
        print(f"Excluindo visitante {visitante.nome_completo}...")
        visitante.delete()
        print("Exclusão concluída com sucesso!")
        
        # Verificar se realmente foi excluído
        if not Visitante.objects.filter(id=visitante_id).exists():
            print(f"Confirmado: Visitante ID {visitante_id} não existe mais no banco de dados.")
        else:
            print(f"ERRO: Visitante ID {visitante_id} ainda existe no banco de dados!")
    else:
        print("Operação cancelada pelo usuário.")
        
except Visitante.DoesNotExist:
    print(f"Visitante com ID {visitante_id} não encontrado.")
except Exception as e:
    print(f"Erro: {str(e)}") 