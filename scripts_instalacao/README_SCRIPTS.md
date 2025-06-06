# Scripts de Instalação SIGEPE

Scripts para facilitar a instalação e execução do sistema SIGEPE.

## Pré-requisitos

1. Python 3.9 ou superior (testado com Python 3.13.2)
2. Windows 10/11
3. Navegador moderno

## Instalação

### Passo 1: Instalar o Sistema

1. Execute `instalar.bat`
   - O script vai:
     1. Verificar requisitos do Python
     2. Criar ambiente virtual
     3. Instalar dependências do sistema
     4. Configurar banco de dados

2. Execute `iniciar.bat`
   - Inicia o servidor
   - Abre acesso ao sistema

## Detalhes dos Scripts

### instalar.bat
Script principal de instalação:
- Verifica versão do Python
- Cria ambiente virtual
- Instala dependências
- Configura banco de dados
- Oferece criação de superusuário

### iniciar.bat
Inicia o sistema:
1. Ativa ambiente virtual
2. Verifica/aplica migrações
3. Inicia servidor Django

## Solução de Problemas

Se encontrar erros:
1. Certifique-se que o Python 3.9+ está instalado e nas variáveis de ambiente
2. Verifique se há espaço suficiente em disco
3. Execute `instalar.bat` novamente se necessário
4. Verifique o arquivo `requirements.txt` para dependências específicas

## Versões das Dependências

- Python: 3.9 ou superior (testado com 3.13.2)
- Django: 5.0 ou superior
- Pillow: 9.5.0 ou superior
- numpy: 1.26.0 ou superior
