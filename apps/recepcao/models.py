from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from datetime import datetime, time

class Setor(models.Model):
    TIPO_CHOICES = [
        ('gabinete_vereador', 'Gabinete'),
        ('departamento', 'Departamento')
    ]
    
    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('primeiro_piso', '1° Piso'),
        ('segundo_piso', '2° Piso'),
    ]

    nome = models.CharField('Nome do Local', max_length=100)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='departamento')
    localizacao = models.CharField('Localização', max_length=20, choices=LOCALIZACAO_CHOICES, default='terreo')
    horario_abertura = models.TimeField('Horário de Abertura', blank=True, null=True)
    horario_fechamento = models.TimeField('Horário de Fechamento', blank=True, null=True)

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.get_localizacao_display()})'

    def esta_aberto(self):
        if not self.horario_abertura or not self.horario_fechamento:
            return None  # Retorna None se não tiver horário definido
            
        agora = timezone.localtime().time()
        return self.horario_abertura <= agora <= self.horario_fechamento

    def status_funcionamento(self):
        esta_aberto = self.esta_aberto()
        if esta_aberto is None:
            return "Horário não definido"
        return "Aberto" if esta_aberto else "Fechado"

class Visitante(models.Model):
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    BAIRROS_CHOICES = [
        ('cidade_nova', 'Cidade Nova'),
        ('primavera', 'Primavera'),
        ('maranhao', 'Maranhão'),
        ('rio_verde', 'Rio Verde'),
        ('nova_vida', 'Nova Vida'),
        ('uniao', 'União'),
        ('liberdade_1', 'Liberdade I'),
        ('liberdade_2', 'Liberdade II'),
        ('da_paz', 'Da Paz'),
        ('caetanopolis', 'Caetanópolis'),
        ('guanabara', 'Guanabara'),
        ('beira_rio_1', 'Beira Rio I'),
        ('beira_rio_2', 'Beira Rio II'),
        ('vila_rica', 'Vila Rica'),
        ('alto_bonito', 'Alto Bonito'),
        ('bethania', 'Bethânia'),
        ('casas_populares', 'Casas Populares'),
        ('nova_carajas', 'Nova Carajás'),
        ('tropical', 'Tropical'),
        ('jardim_canada', 'Jardim Canadá'),
        ('vila_nova', 'Vila Nova'),
        ('novo_brasil', 'Novo Brasil'),
        ('dos_mineiros', 'Dos Mineiros'),
        ('jardim_america', 'Jardim América'),
        ('nova_esperanca', 'Nova Esperança'),
        ('parque_dos_carajas', 'Parque dos Carajás'),
        ('vale_dos_carajas', 'Vale dos Carajás'),
        ('novo_horizonte', 'Novo Horizonte'),
        ('altamira', 'Altamira'),
        ('vila_sao_jose', 'Vila São José'),
        ('alto_boa_vista', 'Alto da Boa Vista'),
        ('outros', 'Outros')
    ]

    nome_completo = models.CharField('Nome Completo', max_length=100)
    nome_social = models.CharField('Nome Social', max_length=100, blank=True, null=True)
    data_nascimento = models.DateField('Data de Nascimento')
    CPF = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato XXX.XXX.XXX-XX'
            )
        ]
    )
    telefone = models.CharField(
        'Telefone',
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (XX) XXXXX-XXXX'
            )
        ]
    )
    email = models.EmailField('E-mail', blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES)
    cidade = models.CharField('Cidade', max_length=100)
    bairro = models.CharField('Bairro', max_length=50, choices=BAIRROS_CHOICES, default='outros')
    foto = models.ImageField('Foto', upload_to='visitantes/', blank=True, null=True)

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['nome_completo']

    def __str__(self):
        if self.nome_social:
            return f"{self.nome_social} ({self.nome_completo})"
        return self.nome_completo

    def clean(self):
        if not self.nome_completo:
            raise ValidationError({'nome_completo': 'O nome completo é obrigatório.'})
        if not self.CPF:
            raise ValidationError({'CPF': 'O CPF é obrigatório.'})
        if not self.telefone:
            raise ValidationError({'telefone': 'O telefone é obrigatório.'})
        if not self.cidade:
            raise ValidationError({'cidade': 'A cidade é obrigatória.'})
        if not self.bairro:
            raise ValidationError({'bairro': 'O bairro é obrigatório.'})

class Visita(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ]

    OBJETIVO_CHOICES = [
        ('reuniao', 'Reunião'),
        ('entrega', 'Entrega'),
        ('manutencao', 'Manutenção'),
        ('evento', 'Evento'),
        ('outros', 'Outros')
    ]

    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('plenario', 'Plenário'),
        ('primeiro_piso', '1° Piso'),
        ('segundo_piso', '2° Piso')
    ]

    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.PROTECT,
        verbose_name='Visitante'
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        verbose_name='Setor'
    )
    localizacao = models.CharField(
        'Localização',
        max_length=20,
        choices=LOCALIZACAO_CHOICES,
        default='terreo'
    )
    objetivo = models.CharField(
        'Objetivo',
        max_length=20,
        choices=OBJETIVO_CHOICES,
        default='outros'
    )
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    data_entrada = models.DateTimeField(
        'Data/Hora de Entrada',
        default=timezone.now
    )
    data_saida = models.DateTimeField(
        'Data/Hora de Saída',
        blank=True,
        null=True
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='em_andamento'
    )

    def clean(self):
        if self.status == 'finalizada' and not self.data_saida:
            raise ValidationError({
                'data_saida': 'Data/Hora de Saída é obrigatória para visitas finalizadas'
            })

    def __str__(self):
        return f'{self.visitante} - {self.setor}'

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-data_entrada']
