from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

# Opções de cores conforme o padrão DETRAN
COR_VEICULO_CHOICES = [
    ("Amarela", "Amarela"),
    ("Azul", "Azul"),
    ("Bege", "Bege"),
    ("Branca", "Branca"),
    ("Cinza", "Cinza"),
    ("Dourada", "Dourada"),
    ("Grena", "Grená"),
    ("Laranja", "Laranja"),
    ("Marrom", "Marrom"),
    ("Prata", "Prata"),
    ("Preta", "Preta"),
    ("Rosa", "Rosa"),
    ("Roxa", "Roxa"),
    ("Verde", "Verde"),
    ("Vermelha", "Vermelha"),
    ("Fantasia", "Fantasia"),
]

# Opções de tipo de veículo
TIPO_VEICULO_CHOICES = [
    ("Carro", "Carro"),
    ("Moto", "Moto"),
    ("Caminhonete", "Caminhonete"),
    ("Caminhão", "Caminhão"),
    ("Ônibus", "Ônibus"),
    ("Outros", "Outros"),
]

class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('presente', 'Presente no Estacionamento'),
        ('saida', 'Saída Realizada'),
    ]

    placa = models.CharField('Placa', max_length=8, unique=True)
    modelo = models.CharField(max_length=50, verbose_name="Modelo do Veículo")
    cor = models.CharField(max_length=15, choices=COR_VEICULO_CHOICES, verbose_name="Cor do Veículo")
    tipo = models.CharField(max_length=15, choices=TIPO_VEICULO_CHOICES, verbose_name="Tipo de Veículo")
    responsavel = models.CharField('Responsável', max_length=100)
    horario_entrada = models.DateTimeField('Horário de Entrada', auto_now_add=True)
    horario_saida = models.DateTimeField('Horário de Saída', null=True, blank=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='presente')
    observacoes = models.TextField('Observações', null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-horario_entrada']

    def __str__(self):
        return f'{self.placa} - {self.responsavel}'

    def clean(self):
        # Validação da placa
        if self.placa:
            self.placa = self.placa.upper()  # Converte para maiúsculas
            if not self.validar_placa(self.placa):
                raise ValidationError({
                    'placa': "Formato de placa inválido. Use o padrão antigo (ABC-1234) ou Mercosul (ABC1D23)."
                })
        
        # Validação dos horários
        if self.horario_saida and self.horario_entrada and self.horario_saida < self.horario_entrada:
            raise ValidationError({
                'horario_saida': "O horário de saída não pode ser anterior ao horário de entrada."
            })

    @staticmethod
    def validar_placa(placa):
        padrao_antigo = r"^[A-Z]{3}-\d{4}$"  # Exemplo: ABC-1234
        padrao_mercosul = r"^[A-Z]{3}\d[A-Z]\d{2}$"  # Exemplo: ABC1D23
        return bool(re.match(padrao_antigo, placa) or re.match(padrao_mercosul, placa))

    def save(self, *args, **kwargs):
        self.clean()  # Executa as validações
        
        # Atualiza o status baseado no horário de saída
        if self.horario_saida:
            self.status = 'saida'
        else:
            self.status = 'presente'
            
        super().save(*args, **kwargs)

'''class Movimentacaoveiculo(models.Model): #adicionando a classe Movimentaçãoveiculo
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    horario_entrada = models.DateTimeField(default=timezone.now)
    horario_saida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.veiculo} - {self.horario_entrada}"
        '''
