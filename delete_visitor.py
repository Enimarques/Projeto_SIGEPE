"""
Script para excluir visitante e seu histórico de visitas
"""
from django.db import transaction
from apps.recepcao.models import Visitante, Visita

def excluir_visitante_com_historico(id_visitante):
    """
    Exclui um visitante e todo o seu histórico de visitas.
    
    Args:
        id_visitante (int): ID do visitante a ser excluído
        
    Returns:
        dict: Resultado da operação com estatísticas
    """
    try:
        with transaction.atomic():
            # Encontra o visitante
            try:
                visitante = Visitante.objects.get(id=id_visitante)
            except Visitante.DoesNotExist:
                return {
                    'sucesso': False,
                    'mensagem': f"Visitante com ID {id_visitante} não encontrado."
                }
            
            # Guarda informações para o log
            nome_visitante = visitante.nome_completo
            
            # Conta e exclui as visitas associadas
            visitas = Visita.objects.filter(visitante=visitante)
            num_visitas = visitas.count()
            
            if num_visitas > 0:
                # Lista as visitas para confirmação
                print(f"Visitante: {nome_visitante} (ID: {id_visitante})")
                print(f"Visitas a serem excluídas: {num_visitas}")
                print("-" * 50)
                
                for i, visita in enumerate(visitas, 1):
                    info_destino = visita.destino.nome if hasattr(visita.destino, 'nome') else str(visita.destino)
                    print(f"{i}. Data: {visita.data_entrada}, Destino: {info_destino}")
                
                # Pede confirmação
                confirmacao = input("\nDigite 'SIM' para confirmar a exclusão: ")
                if confirmacao.upper() != "SIM":
                    return {
                        'sucesso': False,
                        'mensagem': "Operação cancelada pelo usuário."
                    }
                
                # Excluir as visitas
                visitas.delete()
            
            # Excluir o visitante
            visitante.delete()
            
            return {
                'sucesso': True,
                'mensagem': f"Visitante {nome_visitante} e {num_visitas} visitas excluídos com sucesso."
            }
    
    except Exception as e:
        return {
            'sucesso': False,
            'mensagem': f"Erro ao excluir: {str(e)}"
        }

# Função para uso interativo
def executar_exclusao():
    try:
        id_visitante = int(input("Digite o ID do visitante que deseja excluir: "))
        resultado = excluir_visitante_com_historico(id_visitante)
        
        if resultado['sucesso']:
            print("\n✅ " + resultado['mensagem'])
        else:
            print("\n❌ " + resultado['mensagem'])
    
    except ValueError:
        print("\n❌ ID inválido. Digite um número inteiro.")
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")

if __name__ == "__main__":
    # Se executado diretamente como script
    executar_exclusao() 