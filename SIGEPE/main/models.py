#espaço para as importaçoes do projeto

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import get_current_timezone

#CRIANDO TABELA VISITANTES E SETORES
class Pessoa(models.Model):
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
  
'''class visitas(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    data_saida = models.DateTimeField(auto_now_add=True)
    local_saida = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.visitante.nome} - {self.local_saida}'''
    
class Setor(models.Model):
  nome = models.CharField(max_length=100, unique=True)
  localização = models.CharField(max_length=255)
  ramal = models.CharField(max_length=20)
  disponibilidade = models.BooleanField(default=True) #ACEITA ABERTO OU FECHADO, TRUE OR FALSE
  
  def __str__(self):
      return self.nome

    
# CRIAÇÃO DOS TIPOS DE USUÁRIOS 

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('RECEP', 'Recepcionista'),
    ]
    
    usuario = models.CharField(max_length=50, unique=True)  # Nome de login
    senha = models.CharField(max_length=255)  # Senha criptografada
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='RECEP')

    def set_senha(self, senha_plana):
        """Criptografa e define a senha."""
        self.senha = make_password(senha_plana)

    def verificar_senha(self, senha_plana):
        """Verifica se a senha está correta."""
        return check_password(senha_plana, self.senha)

    def __str__(self):
        return f"{self.usuario} ({self.get_tipo_display()})"
    


#CRIAÇÃO DA CLASSE DE VEÍCULOS

class Veiculo(models.Model):
   STATUS_CHOICES = [
      ('ENTRADA', 'Dentro do estacionamento')
      ('SAIDA', 'Fora do estacionamento')
   ]

   placa = models.CharField(max_length=10, unique=True)
   responsavel = models.CharField(max_length=80)
   horario_entrada = models.DateTimeField(auto_now_add=True)
   horario_saida = models.DateTimeField(blank=True, null=True)
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ENTRADA') 
   
   def __str__(self):
      return f'{self.placa}'