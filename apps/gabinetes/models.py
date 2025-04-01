from django.db import models
from django.utils import timezone
from apps.recepcao.models import Assessor, Setor

class Gabinete(models.Model):
    """
    Modelo para representar um Gabinete de Vereador
    """
    nome = models.CharField('Nome', max_length=100)
    vereador = models.CharField('Vereador', max_length=100)
    setor = models.OneToOneField(
        Setor,
        on_delete=models.PROTECT,
        related_name='gabinete',
        verbose_name='Setor',
        limit_choices_to={'tipo': 'gabinete_vereador'}
    )
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    email = models.EmailField('E-mail', blank=True, null=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Gabinete'
        verbose_name_plural = 'Gabinetes'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.vereador}"
