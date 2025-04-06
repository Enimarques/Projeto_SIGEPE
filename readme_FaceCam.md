# Módulo de Reconhecimento Facial - SIGEPE

Este documento descreve o módulo de reconhecimento facial do SIGEPE (Sistema de Gestão de Pessoas e Veículos), incluindo sua instalação, configuração e utilização.

## Índice
1. [Requisitos](#requisitos)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Utilização](#utilização)
5. [Interface do Usuário](#interface-do-usuário)
6. [Solução de Problemas](#solução-de-problemas)

## Requisitos

### Hardware
- Webcam física (não virtual) funcional
- Processador com suporte a instruções SSE4 ou superior
- Mínimo de 4GB de RAM
- Boa iluminação para captura de fotos

### Software
- Python 3.10
- Visual Studio Build Tools 2022 (com suporte C++)
- CMake
- Navegador moderno com suporte a WebRTC

## Instalação

1. **Preparação do Ambiente**
   ```bash
   # Criar e ativar ambiente virtual
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instalação das Dependências**
   ```bash
   # Atualizar pip
   pip install --upgrade pip setuptools wheel

   # Instalar dependências principais
   pip install dlib==19.24.6
   pip install face_recognition
   pip install opencv-python
   pip install mediapipe
   ```

3. **Verificação da Instalação**
   ```bash
   # Testar se as bibliotecas foram instaladas corretamente
   python test_face_recognition.py
   ```

## Configuração

1. **Configuração do Django**
   
   Certifique-se de que as seguintes configurações estão presentes no `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'apps.recepcao',
   ]

   # Configurações de mídia para fotos dos visitantes
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

2. **Configuração do Modelo de Visitante**
   
   O modelo Visitante já inclui os campos necessários:
   - `foto`: Campo para armazenar a foto do visitante
   - `face_id`: Identificador único do rosto
   - `face_registrada`: Status do registro facial

## Utilização

### 1. Registro de Novo Visitante

1. Acesse o sistema como administrador
2. Navegue até "Recepção > Cadastro de Visitantes"
3. Preencha os dados do visitante
4. Use a câmera para capturar uma foto clara do rosto:
   - Posicione o rosto dentro do guia circular
   - Mantenha uma expressão neutra
   - Garanta boa iluminação
   - Evite óculos escuros ou chapéus

### 2. Registro Facial

1. Na página do visitante, clique em "Registrar Face"
2. O sistema processará a foto e registrará o padrão facial
3. Uma mensagem de sucesso será exibida quando concluído
4. O status será atualizado com um indicador verde

### 3. Reconhecimento em Tempo Real

1. Acesse "Recepção > Reconhecimento Facial"
2. A câmera será ativada automaticamente
3. O sistema exibirá:
   - Caixas verdes ao redor dos rostos reconhecidos
   - Nome do visitante quando identificado
   - Status "Desconhecido" para rostos não cadastrados

## Interface do Usuário

### 1. Captura de Foto
- Interface moderna com guia circular para posicionamento
- Indicadores visuais de status (verde/amarelo)
- Botões claros para captura e cancelamento
- Feedback visual do status da câmera

### 2. Seleção de Setor
- Campos de seleção intuitivos usando Select2
- Organização hierárquica (Tipo de Setor > Setor)
- Opções predefinidas e organizadas
- Validação em tempo real

### 3. Feedback Visual
- Fotos em formato circular para melhor apresentação
- Indicadores de status do reconhecimento
- Mensagens claras de erro/sucesso
- Guias visuais para posicionamento

## Solução de Problemas

### Problemas Comuns

1. **Erro na Instalação do dlib**
   - Verifique se o Visual Studio Build Tools está instalado
   - Certifique-se de ter o CMake instalado e no PATH
   - Use Python 3.10 (versão recomendada)

2. **Câmera não Detectada**
   - Verifique se está usando uma câmera física (não virtual)
   - Confirme as permissões do navegador
   - Desative todas as câmeras virtuais (OBS, ManyCam, etc.)
   - Reinicie o servidor Django

3. **Reconhecimento Não Funciona**
   - Verifique se a foto do visitante é clara e frontal
   - Certifique-se de que o registro facial foi concluído
   - Verifique a iluminação do ambiente
   - Evite movimentos bruscos durante a captura

### Logs e Diagnóstico

Para ativar logs detalhados, adicione ao `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug_facial.log',
        },
    },
    'loggers': {
        'apps.recepcao.face_recognition_manager': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Suporte

Para suporte adicional ou relatar problemas:
1. Abra uma issue no repositório do projeto
2. Inclua logs relevantes
3. Descreva o ambiente (versões de Python, dlib, etc.)
4. Forneça passos para reproduzir o problema
5. Inclua screenshots se relevante
