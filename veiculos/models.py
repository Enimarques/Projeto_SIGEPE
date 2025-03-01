from django.db import models
from django.utils import timezone

class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('dentro', 'Dentro'),
        ('fora', 'Fora'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    responsavel = models.CharField(max_length=100)
    horario_entrada = models.DateTimeField(default=timezone.now)
    horario_saida = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='dentro')

    def __str__(self):
        return f"{self.placa} - {self.responsavel}"
