from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging
from .models import Visitante
from .views import carregar_vetores_faciais

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Visitante)
def atualizar_vetores_faciais_em_memoria(sender, instance, **kwargs):
    """
    Recarrega os vetores faciais na memória sempre que um 
    visitante é salvo ou deletado.
    """
    try:
        logger.info(f"Signal recebido do visitante {instance.id}. Recarregando vetores faciais...")
        carregar_vetores_faciais()
    except Exception as e:
        logger.error(f"Erro ao recarregar vetores faciais após salvar/deletar visitante {instance.id}: {e}", exc_info=True) 