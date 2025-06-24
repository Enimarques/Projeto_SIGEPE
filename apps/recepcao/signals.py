from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Visitante
from .views import carregar_vetores_faciais

@receiver([post_save, post_delete], sender=Visitante)
def atualizar_vetores_faciais_em_memoria(sender, instance, **kwargs):
    """
    Recarrega os vetores faciais na memória sempre que um 
    visitante é salvo ou deletado.
    """
    print(f"Signal recebido do visitante {instance.id}. Recarregando vetores faciais...")
    carregar_vetores_faciais() 