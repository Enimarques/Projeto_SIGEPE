# Scripts de Instalação SIGEPE

Scripts para facilitar a instalação e execução do sistema SIGEPE, especialmente o módulo de reconhecimento facial.

## Pré-requisitos

1. Python 3.9 ou superior (testado com Python 3.13.2)
2. Windows 10/11
3. Visual Studio Build Tools 2022 com suporte C++ (necessário para reconhecimento facial)
4. Navegador moderno com suporte a WebRTC (para webcam)

## Ordem de Instalação

### Passo 1: Verificar Requisitos
Execute `verificar_requisitos.bat` para confirmar se seu sistema está pronto para a instalação.

### Passo 2: Escolha o Tipo de Instalação

#### Para Instalação Completa (Recomendado):
1. Instale o Visual Studio Build Tools 2022 (se ainda não tiver)
   - Baixe em: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Durante a instalação, selecione "Desenvolvimento para desktop com C++"

2. Execute `instalar.bat`
   - Escolha opção 1 (Instalação Completa)
   - O script vai:
     1. Verificar requisitos
     2. Criar ambiente virtual
     3. Chamar automaticamente `instalar_face_recognition.bat`
     4. Instalar dependências do sistema
     5. Configurar banco de dados

3. Execute `iniciar.bat`
   - Inicia o servidor
   - Abre acesso ao sistema

#### Para Instalação Básica (Sem Reconhecimento Facial):
1. Execute `instalar.bat`
   - Escolha opção 2 (Instalação Básica)
   
2. Execute `iniciar.bat`

## Detalhes dos Scripts

### verificar_requisitos.bat
Verifica se todos os pré-requisitos estão instalados:
- Python 3.9+
- Visual Studio Build Tools
- CMake

### instalar.bat
Script principal que oferece:
1. Instalação Completa (Sistema + Reconhecimento Facial)
2. Instalação Básica (Apenas Sistema)

### instalar_face_recognition.bat
Instala componentes do reconhecimento facial:
1. Verifica/instala CMake
2. Instala dlib (19.24.0+)
3. Instala face_recognition (1.3.0+)
4. Instala OpenCV (4.8.0+)
5. Configura modelos faciais

### iniciar.bat
Inicia o sistema:
1. Ativa ambiente virtual
2. Verifica/aplica migrações
3. Inicia servidor Django

## Solução de Problemas

Se encontrar erros:
1. Execute `verificar_requisitos.bat` para diagnosticar problemas
2. Certifique-se que o Visual Studio Build Tools está instalado (para reconhecimento facial)
3. Verifique se o Python 3.9+ está nas variáveis de ambiente
4. Tente reiniciar o computador após instalar o Visual Studio Build Tools
5. Execute `instalar.bat` novamente se necessário

## Versões das Dependências

- Python: 3.9 ou superior (testado com 3.13.2)
- dlib: 19.24.0 ou superior
- face-recognition: 1.3.0 ou superior
- opencv-python: 4.8.0 ou superior
- numpy: 1.24.0 ou superior
