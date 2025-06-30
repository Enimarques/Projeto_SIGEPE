# Arquitetura Técnica do Modo Totem

A implementação do Modo Totem segue uma arquitetura cliente-servidor moderna, onde o frontend (rodando no navegador do totem) se comunica com o backend (Django) através de APIs REST, utilizando tecnologias avançadas de IA para reconhecimento facial.

## Frontend

O frontend é composto por uma série de templates HTML responsivos, estilizados com CSS moderno e controlados por JavaScript ES6+ com módulos.

### **Templates Principais:**
-   **`base_totem.html`**: Template base que inclui Bootstrap 5, Font Awesome e define a estrutura responsiva da interface.
-   **`totem_welcome.html`**: Página inicial com design elegante, logo e botões de navegação principais.
-   **`totem_identificacao.html`**: Página de reconhecimento facial com câmera de alta resolução e overlay visual em tempo real.
-   **`totem_destino.html`**: Interface de seleção de destino com dados do visitante reconhecido.
-   **`totem_finalize_search.html`**: Página dual para finalizar visitas (reconhecimento facial + busca por texto).
-   **`totem_comprovante.html`**: Comprovante final com impressão automática e botões de ação.

### **JavaScript Modular (ES6+ Modules):**
-   **MediaPipe Integration**: Utiliza `@mediapipe/tasks-vision` via CDN para detecção facial avançada.
-   **Gerenciamento de Estado**: Controle robusto de estados de reconhecimento, pausas e timeouts.
-   **Overlay Visual Dinâmico**: Canvas HTML5 com desenho de cantos coloridos ao redor dos rostos detectados.
-   **Feedback em Tempo Real**: Sistema de mensagens dinâmicas com cores e emojis para guiar o usuário.
-   **RequestAnimationFrame**: Loop otimizado de detecção para máxima performance.

### **CSS Responsivo e Moderno:**
-   **Design System**: Gradientes consistentes, tipografia moderna com Poppins e componentes reutilizáveis.
-   **Responsividade Completa**: Breakpoints específicos para diferentes resoluções de totem.
-   **Efeitos Visuais**: Transições suaves, animações de escala e backdrop-filter para feedback elegante.
-   **Print Styles**: Regras específicas para impressão de etiquetas 60x40mm sem interferência.

## Backend (Django)

O backend gerencia a lógica de negócio avançada, interação com banco de dados otimizada e expõe APIs REST robustas para o frontend.

### **Views Principais (`apps/recepcao/views.py`):**

#### **Páginas do Totem:**
-   **`totem_welcome`**: Página inicial elegante com navegação principal e design consistente.
-   **`totem_identificacao`**: Renderiza interface de reconhecimento facial com feedback visual avançado.
-   **`totem_destino`**: Seleção de destino com dados contextuais do visitante reconhecido.
-   **`totem_finalize_search`**: Página dual para finalização de visitas (facial + busca manual).
-   **`totem_comprovante`**: Comprovante com impressão automática de etiquetas 60x40mm.

#### **APIs REST:**
-   **`api_reconhecer_rosto`**: Endpoint principal de reconhecimento facial que recebe imagem Base64, processa com `face_recognition` e retorna dados do visitante.
-   **`api_registrar_visita_totem`**: Criação de registros de visita com validação e logging.
-   **`api_buscar_visitante_ativo`**: Busca por visitantes com visitas em andamento (nome, CPF, nome social).
-   **`api_finalizar_visitas`**: Finalização automática de todas as visitas ativas de um visitante.
-   **`api_get_setores`**: Listagem de setores/gabinetes disponíveis para visita.

### **Sistema de URLs (`apps/recepcao/urls.py`):**
```python
# Rotas do Totem
path('totem/welcome/', views.totem_welcome, name='totem_welcome'),
path('totem/finalize_search/', views.totem_finalize_search, name='totem_finalize_search'),
path('totem/', views.totem_identificacao, name='totem_identificacao'),
path('totem/destino/', views.totem_destino, name='totem_destino'),
path('totem/comprovante/<int:visita_id>/', views.totem_comprovante, name='totem_comprovante'),

# API Endpoints
path('api/reconhecer-rosto/', views.api_reconhecer_rosto, name='api_reconhecer_rosto'),
path('api/registrar-visita/', views.api_registrar_visita_totem, name='api_registrar_visita_totem'),
path('api/buscar-visitante-ativo/', views.api_buscar_visitante_ativo, name='api_buscar_visitante_ativo'),
path('api/finalizar-visitas/', views.api_finalizar_visitas, name='api_finalizar_visitas'),
```

### **Models Otimizados (`apps/recepcao/models.py`):**
-   **`Visitante`**: Dados cadastrais com `biometric_vector` para reconhecimento facial e fotos em múltiplas resoluções.
-   **`Visita`**: Registro completo de visitas com timestamps, status e relacionamentos com visitantes e setores.
-   **`Setor`**: Departamentos e gabinetes com informações de localização e tipo.

### **Funcionalidades Avançadas:**
-   **Processamento de Imagens**: Redimensionamento automático e geração de thumbnails.
-   **Vetores Biométricos**: Geração e comparação usando `face_recognition` com tolerância configurável.
-   **Logging Detalhado**: Rastreamento de todas as ações do totem para auditoria.
-   **Validação Robusta**: Verificação de dados e tratamento de erros abrangente. 