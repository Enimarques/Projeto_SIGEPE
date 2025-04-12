# Guia de Instalação e Configuração do SIGEPE

Este guia detalha o passo a passo para instalar e configurar o sistema SIGEPE completo, com ênfase especial na configuração correta do reconhecimento facial.

## Pré-requisitos

### 1. Instalar Software Base
- Python 3.12 ([Download](https://www.python.org/downloads/))
  - **IMPORTANTE:** Marque a opção "Add Python to PATH" durante a instalação

- Visual Studio Build Tools ([Download](https://visualstudio.microsoft.com/visual-cpp-build-tools/))
  - Selecione "Desktop development with C++"

- CMake ([Download](https://cmake.org/download/))
  - Escolha o instalador Windows x64
  - Marque "Add CMake to the system PATH" durante a instalação

- Git ([Download](https://git-scm.com/downloads))

## Instalação do Sistema

### 1. Clonar o Repositório

```bash
git clone https://github.com/TersanPlay/Urutal.git
cd Urutal
```

### 2. Configurar o Ambiente Virtual

```bash
# Criar ambiente virtual
py -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate
```

### 3. Instalar Dependências na Ordem Correta

**IMPORTANTE:** A ordem de instalação é crucial para o funcionamento correto do reconhecimento facial.

```bash
# 1. Instalar cmake primeiro
py -m pip install cmake

# 2. Instalar dlib 
py -m pip install dlib

# 3. Instalar demais dependências
py -m pip install -r requirements.txt

# 4. Instalar face_recognition_models diretamente do GitHub (CRUCIAL)
py -m pip install git+https://github.com/ageitgey/face_recognition_models
```

### 4. Verificar Instalação do Reconhecimento Facial

Execute este comando para verificar se a instalação foi bem-sucedida:

```bash
py -c "import face_recognition; import face_recognition_models; print('Bibliotecas instaladas com sucesso!')"
```

### 5. Configurar o Banco de Dados

```bash
# Aplicar migrações
py manage.py migrate

# Criar superusuário (opcional)
py manage.py createsuperuser
```

### 6. Ajustar Configurações do Reconhecimento Facial

Edite o arquivo `SIGEPE/settings.py` e verifique/adicione a configuração para o reconhecimento facial:

```python
# Configurações específicas para reconhecimento facial
FACE_RECOGNITION_SETTINGS = {
    'MIN_FACE_CONFIDENCE': 0.6,  # Confiança mínima para reconhecimento
    'FRAME_RESIZE_FACTOR': 0.25,  # Fator de redimensionamento para performance
    'MAX_CONCURRENT_RECOGNITIONS': 5,  # Máximo de rostos simultâneos
    'PHOTOS_SUBDIR': 'fotos_visitantes',  # Subdiretório para fotos
    'ENABLED': True,  # Reconhecimento facial ativado
}
```

Se o sistema estiver travando durante o reconhecimento facial, você pode temporariamente desativá-lo mudando para `'ENABLED': False`.

### 7. Verificar o Arquivo FaceRecognitionManager

Certifique-se de que o arquivo `apps/recepcao/face_recognition_manager.py` tem a verificação do estado de ativação. Adicione o seguinte código no início da classe:

```python
def __init__(self, tolerance=0.6):
    self.known_face_encodings = []
    self.known_face_ids = []
    self.tolerance = tolerance  # Tolerância para reconhecimento (menor = mais preciso)
    self.enabled = settings.FACE_RECOGNITION_SETTINGS.get('ENABLED', True)
    self.load_known_faces()
    print(f"FaceRecognitionManager inicializado com {len(self.known_face_encodings)} faces conhecidas")
    print(f"Reconhecimento facial está {'HABILITADO' if self.enabled else 'DESABILITADO'}")
```

E modifique os métodos principais para verificar se o reconhecimento está ativado:

```python
def load_known_faces(self):
    """Carrega todos os rostos registrados do banco de dados"""
    if not self.enabled:
        print("Reconhecimento facial desabilitado. Não carregando faces...")
        return
    # ... restante do código ...

def register_face(self, visitante_id):
    """Registra um novo rosto para um visitante"""
    if not self.enabled:
        print("Reconhecimento facial desabilitado. Simulando registro com sucesso...")
        visitante = Visitante.objects.get(id=visitante_id)
        visitante.face_registrada = True
        visitante.face_id = str(datetime.now().timestamp())
        visitante.save()
        return True
    # ... restante do código ...

def identify_face(self, frame, tolerance=None):
    """Identifica rostos em um frame de vídeo"""
    if not self.enabled:
        print("Reconhecimento facial desabilitado. Retornando sem identificação...")
        return [], []
    # ... restante do código ...
```

### 8. Iniciar o Servidor

```bash
# Iniciar o servidor Django
py manage.py runserver
```

## Solução de Problemas Comuns

### Erro face_recognition_models

Se aparecer a mensagem:
```
Please install `face_recognition_models` with this command before using `face_recognition`:
pip install git+https://github.com/ageitgey/face_recognition_models
```

Siga estes passos:

1. Parar o servidor (CTRL+C)
2. Desinstalar os pacotes relacionados:
   ```bash
   py -m pip uninstall face_recognition face_recognition_models dlib -y
   ```
3. Reinstalar na ordem correta:
   ```bash
   py -m pip install cmake
   py -m pip install dlib
   py -m pip install face_recognition
   py -m pip install git+https://github.com/ageitgey/face_recognition_models --force-reinstall
   ```

### Problemas de Desempenho com Reconhecimento Facial

Se o sistema estiver travando ou muito lento ao usar o reconhecimento facial:

1. Edite o arquivo `SIGEPE/settings.py` e altere:
   ```python
   'ENABLED': False,  # Temporariamente desativar o reconhecimento facial
   ```

2. Reinicie o servidor

3. Quando o problema for resolvido, você pode reativar o reconhecimento alterando para `'ENABLED': True`

### Problemas de Acesso à Câmera

- Verifique se seu navegador tem permissão para acessar a câmera
- Tente usar o Google Chrome, que geralmente tem melhor suporte para WebRTC
- Verifique se não há outros aplicativos usando a câmera

## Acessando o Sistema

Após iniciar o servidor, acesse o sistema em:
http://127.0.0.1:8000/ ou http://localhost:8000/ 