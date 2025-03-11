from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.core.exceptions import ValidationError
import re

#CRIANDO TABELA PESSOA E SETORES
class Setor(models.Model):
    TIPO_CHOICES = [
        ('gabinete_vereador', 'Gabinete de Vereador'),
        ('departamento', 'Departamento')
    ]
    
    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('plenarinho', 'Plenarinho/Térreo'),
        ('primeiro_piso', '1° Piso'),
        ('segundo_piso', '2° Piso')
    ]
    
    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='departamento')
    localizacao = models.CharField('Localização', max_length=20, choices=LOCALIZACAO_CHOICES, default='terreo')
    is_vereador = models.BooleanField('É Vereador', default=False)
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['tipo', 'nome']

    def __str__(self):
        if self.is_vereador:
            return f"Vereador(a) {self.nome} - {self.get_localizacao_display()}"
        return f"{self.get_tipo_display()} - {self.nome} - {self.get_localizacao_display()}"

    def clean(self):
        if self.tipo == 'gabinete_vereador' and not self.is_vereador:
            self.is_vereador = True
        elif self.tipo == 'departamento' and self.is_vereador:
            raise ValidationError('Um departamento não pode ser marcado como vereador.')

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
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    OBJETIVO_CHOICES = [
        ('reuniao', 'Reunião com o Vereador'),
        ('projeto_lei', 'Discussão de Projetos de Lei'),
        ('apoio_proposta', 'Apoio a Proposta de Lei'),
        ('auxilio_encaminhamento', 'Solicitação de Auxílio ou Encaminhamento'),
        ('apresentacao_projeto', 'Apresentação de Projeto ou Ideia'),
        ('pedido_apoio', 'Pedido de Apoio a Causa Social'),
        ('audiencia_publica', 'Participação em Audiência Pública'),
        ('assinatura_documentos', 'Assinatura de Documentos ou Petições'),
        ('visita_institucional', 'Visita Institucional ou Educacional'),
        ('reuniao_assessoria', 'Reunião com Assessoria Parlamentar'),
        ('denuncias_reclamacoes', 'Recebimento de Denúncias ou Reclamações'),
        ('evento_comemoracao', 'Participação em Evento ou Comemoração'),
        ('pedido_visita_obras', 'Pedido de Visita a Obras ou Serviços Públicos'),
        ('entrevista_imprensa', 'Entrevista de Imprensa'),
        ('acompanha_demandas', 'Acompanhamento de Demandas da Comunidade'),
        ('entrega_documentos', 'Entrega de Requerimentos ou Solicitações'),
        ('consultoria_orientacao', 'Consultoria ou Orientação Jurídica'),
        ('outros', 'Outros (Especificar)'),
    ]
    
    nome_completo = models.CharField('Nome Completo', max_length=100)
    nome_social = models.CharField('Nome Social', max_length=100, blank=True, null=True)
    data_nascimento = models.DateField('Data de Nascimento')
    CPF = models.CharField('CPF', max_length=14, unique=True)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.EmailField('E-mail', blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES)
    cidade = models.CharField('Cidade', max_length=100)
    foto = models.ImageField('Foto', upload_to='fotos_visitante/', blank=True, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name='Setor', null=True, blank=True)
    objetivo_visita = models.CharField(
        'Objetivo da Visita',
        max_length=50,
        choices=OBJETIVO_CHOICES,
        default='visita_institucional',  
        null=True,  
        blank=True
    )
    descricao_outros = models.TextField('Descrição (quando Outros)', blank=True, null=True)
    
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
        if not self.objetivo_visita:
            raise ValidationError({'objetivo_visita': 'O objetivo da visita é obrigatório.'})
        if self.objetivo_visita == 'outros' and not self.descricao_outros:
            raise ValidationError({'descricao_outros': 'A descrição é obrigatória quando o objetivo é "Outros".'})

class Visita(models.Model):
    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.PROTECT,
        verbose_name='Visitante',
        null=True,  
        blank=True
    )
    data_visita = models.DateTimeField('Data da Visita', default=timezone.now)
    observacoes = models.TextField('Observações', blank=True, null=True)
    horario_saida = models.DateTimeField('Horário de Saída', blank=True, null=True)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-data_visita']

    def __str__(self):
        if self.visitante:
            return f'Visita de {self.visitante} em {self.data_visita.strftime("%d/%m/%Y %H:%M")}'
        return f'Visita em {self.data_visita.strftime("%d/%m/%Y %H:%M")}'

    def clean(self):
        if not self.visitante:
            raise ValidationError({'visitante': 'O visitante é obrigatório.'})

    def registrar_saida(self):
        self.horario_saida = timezone.now()
        self.save()
