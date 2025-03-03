#espaço para as importaçoes do projeto

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.timezone import get_current_timezone

#CRIANDO TABELA PESSOA E SETORES
class Visitante(models.Model):
    ESTADOS_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    nome_completo = models.CharField(max_length=70)
    nome_social = models.CharField(max_length=70, blank=True, null=True)
    data_nascimento = models.DateField(blank=True , null=True)  #FORMATO ERRADO, CORRIGIR
    CPF = models.CharField(max_length=14, unique=True)      #depois aprimorar importando o validationerror e validate_docbr import cpf
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=80, null=True , blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES, null=True, blank=True)
    cidade = models.CharField(max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_visitante/')
    data_registro = models.DateTimeField(auto_now_add=True)  #REGISTRA A DATA DE REGISTRO DO USUARIO
    
    def __str__(self):
     return self.nome_completo
  
class Setor(models.Model):
  nome = models.CharField(max_length=100, unique=True)
  localização = models.CharField(max_length=255)
  ramal = models.CharField(max_length=20)
  disponibilidade = models.BooleanField(default=True) #ACEITA ABERTO OU FECHADO, TRUE OR FALSE
  
  class meta:
      db_table = 'setores' 
      verbose_name = 'Setor'
      verbose_name_plural = 'Setores'   
        
  def __str__(self):
      return self.nome

class Visita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='Visitas') #SE EXCLUIR PESSOA, AS VISITAS TBM SERÃO EXCLUIDAS (CASCADE)
    data_entrada = models.DateTimeField (auto_now_add=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='Visitas')
    motivo_visita = models.TextField (blank=True , null=True)
    etiqueta_emitida = models.BooleanField(default=False)
    reconhecimento_facial = models.BooleanField(default=False)
    hora_saida = models.TimeField(blank=True, null=True) 
       
    def __str__(self):
        return f'Visita de {self.visitante} ao setor {self.setor} em {self.data_entrada.strftime("%d-%m-%Y às %H:%M:%S")}'
    
