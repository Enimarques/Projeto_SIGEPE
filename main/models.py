from django.db import models

#CRIANDO TABELA VISITANTES E SETORES
class Visitante(models.Model):
  nome_completo = models.CharField(max_length=70)
  nome_social = models.CharField(max_length=70, blank=True, null=True)
  data_nascimento = models.DateField(blank=True , null=True)  #FORMATO ERRADO, CORRIGIR
  CPF = models.CharField(max_length=14, unique=True)      #depois aprimorar importando o validationerror e validate_docbr import cpf
  foto = models.ImageField(upload_to='fotos_visitante/')
  data_registro = models.DateTimeField(auto_now_add=True)  #REGISTRA A DATA DE REGISTRO DO USUARIO
  
  def __str__(self):
     return self.nome_completo
  
class Setor(models.Model):
  nome = models.CharField(max_length=100, unique=True)
  localização = models.CharField(max_length=255)
  ramal = models.CharField(max_length=20)
  disponibilidade = models.BooleanField(default=True) #ACEITA ABERTO OU FECHADO, TRUE OR FALSE
  
  def __str__(self):
      return self.nome

    
# CRIAÇÃO DOS TIPOS DE USUÁRIOS 

from django.contrib.auth.hashers import make_password, check_password

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
   placa = models.CharField(max_length=10, unique=True)
   horario_entrada = models.DateTimeField(auto_now_add=True)