from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.recepcao.models import Visitante

class Veiculo(models.Model):
    TIPOS_VEICULO = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('van', 'Van/Utilitário'),
        ('caminhao', 'Caminhão'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('presente', 'No Estacionamento'),
        ('saida', 'Saída Realizada'),
    ]
    
    # Informações do Veículo
    placa = models.CharField('Placa', max_length=8)
    tipo = models.CharField('Tipo', max_length=10, choices=TIPOS_VEICULO)
    modelo = models.CharField('Modelo', max_length=50)
    cor = models.CharField('Cor', max_length=30)
    
    # Visitante Responsável
    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
        related_name='veiculos',
        verbose_name='Visitante',
        null=True,  # Permitindo nulo temporariamente
        blank=True
    )
    
    # Registro de Entrada e Saída
    data_entrada = models.DateTimeField('Data de Entrada', default=timezone.now)
    data_saida = models.DateTimeField('Data de Saída', null=True, blank=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='presente')
    observacoes = models.TextField('Observações', blank=True, default='')
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f'{self.placa} - {self.modelo} ({self.get_tipo_display()})'
    
    def clean(self):
        # Validação da placa
        if self.placa:
            self.placa = self.placa.upper()
            if not self.placa.replace('-', '').isalnum():
                raise ValidationError({
                    'placa': "A placa deve conter apenas letras, números e hífen."
                })
        
        # Validação dos horários
        if self.data_saida and self.data_entrada and self.data_saida < self.data_entrada:
            raise ValidationError({
                'data_saida': "A data de saída não pode ser anterior à data de entrada."
            })
    
    def save(self, *args, **kwargs):
        self.clean()  # Executa as validações
        
        # Atualiza o status baseado na data de saída
        if self.data_saida:
            self.status = 'saida'
        else:
            self.status = 'presente'
        
        super().save(*args, **kwargs)
    
    @property
    def esta_no_estacionamento(self):
        return self.data_saida is None
