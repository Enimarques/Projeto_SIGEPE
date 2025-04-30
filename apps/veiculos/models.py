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

    CORES_VEICULO = [
        ('amarela', 'Amarela'),
        ('azul', 'Azul'),
        ('bege', 'Bege'),
        ('branca', 'Branca'),
        ('cinza', 'Cinza'),
        ('dourada', 'Dourada'),
        ('grená', 'Grená'),
        ('laranja', 'Laranja'),
        ('marrom', 'Marrom'),
        ('prata', 'Prata'),
        ('preta', 'Preta'),
        ('rosa', 'Rosa'),
        ('roxa', 'Roxa'),
        ('verde', 'Verde'),
        ('vermelha', 'Vermelha'),
    ]

    STATUS_CHOICES = [
        ('presente', 'No Estacionamento'),
        ('saida', 'Saída Realizada'),
        ('bloqueado', 'Bloqueado'),
    ]
    
    # Informações do Veículo
    placa = models.CharField('Placa', max_length=8)
    tipo = models.CharField('Tipo', max_length=10, choices=TIPOS_VEICULO)
    modelo = models.CharField('Modelo', max_length=50)
    cor = models.CharField('Cor', max_length=20, choices=CORES_VEICULO)
    
    # Informações dos Ocupantes
    nome_condutor = models.CharField('Nome do Condutor', max_length=100, blank=True, null=True)
    nome_passageiro = models.CharField('Nome do Passageiro', max_length=100, blank=True, null=True)
    
    # Visitante Responsável
    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
        related_name='veiculos',
        verbose_name='Visitante',
        null=True,
        blank=True
    )
    
    # Registro de Entrada e Saída
    data_entrada = models.DateTimeField('Data de Entrada', default=timezone.now)
    data_saida = models.DateTimeField('Data de Saída', null=True, blank=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='presente')
    observacoes = models.TextField('Observações', blank=True, default='')
    
    # Novos campos
    bloqueado = models.BooleanField('Bloqueado', default=False)
    motivo_bloqueio = models.TextField('Motivo do Bloqueio', blank=True, null=True)
    data_bloqueio = models.DateTimeField('Data do Bloqueio', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f'{self.placa} - {self.modelo} ({self.get_tipo_display()})'
    
    @staticmethod
    def validar_placa(placa):
        """Valida o formato da placa do veículo"""
        placa = placa.upper().strip()
        
        # Remove qualquer caractere que não seja letra ou número
        placa = ''.join(c for c in placa if c.isalnum())
        
        # Verifica se tem 7 caracteres
        if len(placa) != 7:
            return False
            
        # Verifica se os primeiros 3 caracteres são letras
        if not placa[:3].isalpha():
            return False
            
        # Verifica se os últimos 4 caracteres são números (formato antigo)
        if placa[3:].isdigit():
            return True
            
        # Verifica formato Mercosul (ABC1D23)
        if placa[3].isdigit() and placa[4].isalpha() and placa[5:].isdigit():
            return True
            
        return False
    
    def clean(self):
        # Validação da placa
        if self.placa:
            self.placa = self.placa.upper()
            if not self.validar_placa(self.placa):
                raise ValidationError({
                    'placa': "Formato de placa inválido! Use o padrão antigo (ABC-1234) ou Mercosul (ABC1D23)."
                })
        
        # Validação dos horários
        if self.data_saida and self.data_entrada and self.data_saida < self.data_entrada:
            raise ValidationError({
                'data_saida': "A data de saída não pode ser anterior à data de entrada."
            })
        
        # Validação do bloqueio
        if self.bloqueado and not self.motivo_bloqueio:
            raise ValidationError({
                'motivo_bloqueio': "É necessário informar o motivo do bloqueio."
            })
    
    def save(self, *args, **kwargs):
        self.clean()  # Executa as validações
        
        # Atualiza o status baseado na data de saída e bloqueio
        if self.bloqueado:
            self.status = 'bloqueado'
            if not self.data_bloqueio:
                self.data_bloqueio = timezone.now()
        elif self.data_saida:
            self.status = 'saida'
        else:
            self.status = 'presente'
        
        super().save(*args, **kwargs)
    
    @property
    def esta_no_estacionamento(self):
        return self.data_saida is None

class HistoricoVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='historico')
    data_entrada = models.DateTimeField('Data de Entrada')
    data_saida = models.DateTimeField('Data de Saída', null=True, blank=True)
    visitante = models.ForeignKey(Visitante, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Histórico de Veículo'
        verbose_name_plural = 'Históricos de Veículos'
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_entrada.date()}'
