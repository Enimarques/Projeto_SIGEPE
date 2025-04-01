# Guia de Instalação - SIGEPE

Este guia detalha os passos necessários para instalar e configurar o SIGEPE, especialmente o módulo de reconhecimento facial.

## Requisitos do Sistema

### Windows
- Python 3.12 ou superior
- Visual Studio Build Tools 2019
- CMake
- Git

## Passo a Passo

### 1. Preparação do Ambiente (Windows)

#### Visual Studio Build Tools 2019
1. Baixe em: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Execute o instalador
3. Selecione "Desktop development with C++"
4. Instale

#### CMake
1. Baixe em: https://cmake.org/download/
2. Escolha o instalador Windows x64
3. Durante a instalação, marque "Add CMake to the system PATH"
4. Conclua a instalação

### 2. Configuração do Projeto

1. Clone o repositório:
```bash
git clone https://github.com/Enimarques/Projeto_SIGEPE.git
cd Projeto_SIGEPE
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalação das Dependências

#### Método 1 - Com Visual Studio Build Tools (Recomendado)
```bash
pip install -r requirements.txt
```

#### Método 2 - Usando dlib pré-compilado
```bash
# Baixar dlib
curl -L -o dlib.whl https://github.com/shashankx86/dlib_compiled/raw/main/dlib-19.22.99-cp39-cp39-win_amd64.whl

# Instalar dlib
pip install dlib.whl

# Instalar outras dependências
pip install -r requirements.txt
```

### 3.1. Instalação de Dependências problemas face_recongnitions_models 
rodar o comando "pip3 install setuptools"

### 4. Configuração do Django

1. Aplique as migrações:
```bash
python manage.py migrate
```

2. Crie um superusuário:
```bash
python manage.py createsuperuser
```

3. Execute o servidor:
```bash
python manage.py runserver
```

## Instalação do Projeto SIGEPE

## Requisitos Prévios
- Python 3.12
- pip
- virtualenv

## Instalação do Ambiente Virtual

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

## Instalação de Dependências

### Dependências Principais
```bash
pip install -r requirements.txt
```

### Dependências Específicas para Reconhecimento Facial

#### Instalação do face_recognition_models
```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

#### Requisitos Adicionais
- Certifique-se de ter o CMake instalado
- Para Windows, pode ser necessário instalar o Visual C++ Build Tools

### Solução de Problemas Comuns
- Se encontrar erros com dlib, use o wheel file pré-compilado
- Verifique a compatibilidade das versões de numpy, opencv e face_recognition

## Configuração Inicial
```bash
# Faça as migrações do banco de dados
python manage.py makemigrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser
```

## Executando o Projeto
```bash
python manage.py runserver
```

## Notas para Reconhecimento Facial
- O sistema usa face_recognition, mediapipe e opencv
- Certifique-se de ter uma webcam configurada para testes de reconhecimento facial
- As faces são armazenadas em `media/faces/`

## Verificação da Instalação

1. Acesse http://localhost:8000/admin
2. Faça login com o superusuário
3. Verifique se o módulo de recepção está disponível

## Troubleshooting

### Erro ao instalar dlib
- Certifique-se que o Visual Studio Build Tools está instalado corretamente
- Verifique se o CMake está no PATH do sistema
- Tente usar o arquivo wheel pré-compilado

### Erro de câmera
- Verifique as permissões do navegador
- Teste com outro navegador
- Verifique se a câmera está funcionando em outros aplicativos

### Erro de reconhecimento facial
- Certifique-se que todas as dependências foram instaladas
- Verifique se o dlib está instalado corretamente
- Teste com iluminação adequada

## Dependências Principais

```txt
# Django e frontend
Django>=4.2.0,<5.0.0
django-crispy-forms>=2.0,<3.0
crispy-bootstrap5>=2024.2

# Reconhecimento facial
opencv-python>=4.9.0.80
mediapipe>=0.10.11
face-recognition>=1.3.0
dlib>=19.22.99

# Processamento de imagens
Pillow>=9.5.0,<10.0.0
numpy>=1.26.0

# Outras dependências
python-dotenv>=1.0.0,<2.0.0
qrcode>=7.4.2
```

## Suporte

Se encontrar problemas durante a instalação:
1. Verifique este guia de instalação
2. Consulte a documentação oficial das bibliotecas
3. Abra uma issue no repositório
4. Entre em contato com a equipe de desenvolvimento
