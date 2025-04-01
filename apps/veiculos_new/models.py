from django.db import models

# Create your models here.

class VeiculoTeste(models.Model):
    """Modelo de teste para verificar se aparece no admin."""
    nome = models.CharField('Nome', max_length=100)
    
    class Meta:
        verbose_name = 'Veículo de Teste'
        verbose_name_plural = 'Veículos de Teste'
    
    def __str__(self):
        return self.nome
