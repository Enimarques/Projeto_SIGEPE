# Configuração e Dependências

Para que o Modo Totem e o Reconhecimento Facial funcionem corretamente, é necessário garantir que todas as dependências estejam instaladas e configuradas.

## Dependências de Backend (Python)

Todas as bibliotecas Python necessárias estão listadas no arquivo `requirements.txt`. As mais críticas para esta funcionalidade são:

### **Essenciais:**
-   **`Django`**: Framework web principal com versão compatível.
-   **`Pillow`**: Manipulação avançada de imagens (redimensionamento, thumbnails).
-   **`face-recognition`**: Biblioteca principal para vetores biométricos e comparação facial.
-   **`numpy`**: Operações matemáticas para processamento de vetores e matrizes.
-   **`dlib`** e **`cmake`**: Dependências de baixo nível que podem exigir compiladores C++.

### **Opcionais para Performance:**
-   **`opencv-python`**: Processamento adicional de imagens.
-   **`redis`**: Cache de vetores biométricos para comparação mais rápida.
-   **`celery`**: Processamento assíncrono de imagens pesadas.

### **Instalação:**
```bash
# Instalar dependências principais
pip install -r requirements.txt

# Para sistemas Windows, pode ser necessário:
pip install cmake
pip install dlib

# Para melhor performance:
pip install opencv-python redis celery
```

## Dependências de Frontend (JavaScript)

### **MediaPipe Tasks Vision (Atual):**
O sistema utiliza **MediaPipe** via CDN, eliminando a necessidade de arquivos locais:

```html
<!-- Em cada template que usa reconhecimento facial -->
<script type="module">
import { FaceDetector, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";
</script>
```

### **Dependências de UI:**
-   **Bootstrap 5**: Framework CSS via CDN para interface responsiva
-   **Font Awesome**: Ícones da interface via CDN
-   **Google Fonts**: Tipografia Poppins para design moderno

### **Configuração no `base_totem.html`:**
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Conteúdo -->
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Configuração do Projeto

### **Variáveis de Ambiente:**
```python
# settings.py ou .env
SECRET_KEY = 'sua-secret-key-aqui'
DEBUG = True  # False em produção
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'seu-dominio.com']

# Configurações opcionais para performance
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Configuração de mídia para fotos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### **URLs Principais:**
```python
# SIGEPE/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recepcao/', include('apps.recepcao.urls')),
    # outras URLs...
]

# apps/recepcao/urls.py - Rotas do Totem
urlpatterns = [
    # Páginas do Totem
    path('totem/welcome/', views.totem_welcome, name='totem_welcome'),
    path('totem/', views.totem_identificacao, name='totem_identificacao'),
    path('totem/destino/', views.totem_destino, name='totem_destino'),
    path('totem/finalize_search/', views.totem_finalize_search, name='totem_finalize_search'),
    path('totem/comprovante/<int:visita_id>/', views.totem_comprovante, name='totem_comprovante'),
    
    # APIs
    path('api/reconhecer-rosto/', views.api_reconhecer_rosto, name='api_reconhecer_rosto'),
    path('api/registrar-visita/', views.api_registrar_visita_totem, name='api_registrar_visita_totem'),
    path('api/buscar-visitante-ativo/', views.api_buscar_visitante_ativo, name='api_buscar_visitante_ativo'),
    path('api/finalizar-visitas/', views.api_finalizar_visitas, name='api_finalizar_visitas'),
]
```

### **Banco de Dados:**
```bash
# Migrar banco de dados
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Carregar dados iniciais (se houver)
python manage.py loaddata initial_data.json
```

### **Campos Essenciais nos Models:**
```python
# Visitante
class Visitante(models.Model):
    nome_completo = models.CharField(max_length=200)
    nome_social = models.CharField(max_length=200, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    foto = models.ImageField(upload_to='visitantes/fotos/')
    biometric_vector = models.JSONField(null=True, blank=True)  # ESSENCIAL
    data_cadastro = models.DateTimeField(auto_now_add=True)

# Visita
class Visita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)
    objetivo = models.TextField()
    status = models.CharField(max_length=20, default='ativa')
```

## Configuração de Hardware

### **Câmera:**
-   **Resolução Mínima**: 720p (1280x720)
-   **Resolução Recomendada**: 1080p (1920x1080)
-   **FPS**: 30fps mínimo, 60fps ideal
-   **Formato**: USB ou integrada com drivers atualizados

### **Impressora de Etiquetas:**
-   **Formato**: 60mm x 40mm
-   **Tipo**: Térmica direta ou transferência térmica
-   **Conectividade**: USB ou rede
-   **Driver**: Configurado no sistema operacional

### **Totem/Dispositivo:**
-   **Navegador**: Chrome 90+ ou Edge 90+ (suporte a MediaPipe)
-   **Memória**: 4GB RAM mínimo, 8GB recomendado
-   **Processador**: Dual-core moderno para processamento de IA
-   **Conexão**: Internet estável para CDNs e APIs

## Verificação de Funcionamento

### **Teste do Sistema:**
```bash
# 1. Verificar dependências Python
python -c "import face_recognition, numpy, PIL; print('Backend OK')"

# 2. Testar servidor Django
python manage.py runserver

# 3. Acessar URLs de teste
# http://127.0.0.1:8000/recepcao/totem/welcome/
# http://127.0.0.1:8000/recepcao/totem/
# http://127.0.0.1:8000/recepcao/totem/finalize_search/
```

### **Troubleshooting Comum:**
-   **MediaPipe não carrega**: Verificar conexão com internet e navegador atualizado
-   **Câmera não funciona**: Verificar permissões do navegador e drivers
-   **face_recognition falha**: Instalar/recompilar dlib com ferramentas C++
-   **Overlays não aparecem**: Verificar console do navegador para erros JavaScript 