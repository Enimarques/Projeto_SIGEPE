# Documentação - Página de Finalizar Visita do Totem

## 📋 Visão Geral

A página **Finalizar Visita** do sistema URUTAU permite que visitantes encerrem suas visitas de forma autônoma através do totem, utilizando duas modalidades:

- **🎥 Reconhecimento Facial**: Detecção automática e finalização instantânea
- **⌨️ Busca por Texto**: Pesquisa manual por nome ou CPF

**URL:** `http://127.0.0.1:8000/recepcao/totem/finalize_search/`  
**Template:** `templates/recepcao/totem_finalize_search.html`

---

## 🎨 Interface Visual e Design

### Layout Principal
- **Container**: `.totem-container` com layout flexbox centralizado
- **Logo**: Câmara Municipal (250px, auto-height)
- **Título**: "Finalizar Visita" com gradiente colorido
- **Separador visual**: Linha com gradiente entre título e conteúdo
- **Botão voltar**: Redirecionamento para página welcome

### Estilo Visual Consistente
```css
.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(45deg, #5e72e4, #825ee4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.05);
    line-height: 1.2;
}
```

### Elementos da Interface
- **Campo de busca**: Input centralizado com placeholder "Digite seu Nome ou CPF"
- **Área da câmera**: 640×480px com bordas arredondadas e sombra
- **Status da câmera**: Feedback visual em tempo real
- **Botão voltar**: Estilo consistente com outras páginas do totem

---

## 🔧 Funcionalidades Implementadas

### 1. Sistema Dual de Finalização

#### 🎥 Reconhecimento Facial
- **Tecnologia**: MediaPipe Face Detection
- **Detecção em tempo real** de rostos na câmera
- **Overlay visual** com indicadores coloridos
- **Finalização automática** das visitas quando reconhece o visitante

#### ⌨️ Busca por Texto  
- **Busca dinâmica** com debounce de 500ms
- **Campos aceitos**: Nome completo, nome social, CPF
- **Modal de confirmação** com lista de visitas ativas
- **Validação mínima** de 3 caracteres

### 2. Feedback Visual Avançado

#### Indicadores da Câmera
- **🟡 Amarelo**: Rosto detectado, aproximar mais
- **🟢 Verde**: Rosto na posição ideal, analisando
- **Overlay dinâmico**: Cantos desenhados ao redor do rosto

#### Mensagens de Status
- "Carregando modelo de IA..."
- "Iniciando câmera..."
- "Posicione seu rosto na câmera para finalizar visita"
- "Aproxime-se um pouco mais da câmera"
- "Ótimo! Analisando rosto para finalizar visita..."
- "Reconhecido: [Nome]! Finalizando visitas..."
- "✅ Visitas de [Nome] finalizadas com sucesso!"

---

## 🎯 Fluxo de Uso - Reconhecimento Facial

### 1. Inicialização
```javascript
async function initializeFaceRecognition() {
    // Carrega modelo MediaPipe
    // Inicializa câmera com resolução otimizada
    // Configura canvas overlay
    // Inicia loop de detecção
}
```

### 2. Detecção de Rosto
```javascript
async function detectFacesLoop() {
    // Detecta rostos no frame atual
    // Calcula proximidade (25% da largura mínima)
    // Desenha overlay colorido
    // Atualiza mensagens de status
}
```

### 3. Reconhecimento e Finalização
```javascript
async function sendFrameForRecognition() {
    // Captura frame da câmera
    // Envia para API de reconhecimento
    // Processa resposta
    // Chama finalização automática
}
```

### 4. Finalização Automática
```javascript
async function finalizeVisitsByFaceRecognition(visitanteId, nomeVisitante) {
    // Chama API de finalização
    // Processa resultado
    // Exibe mensagem de sucesso
    // Redireciona após 2 segundos
}
```

---

## 📝 Fluxo de Uso - Busca por Texto

### 1. Busca Dinâmica
- **Input com debounce** de 500ms para otimizar requisições
- **Validação mínima** de 3 caracteres
- **Spinner visual** durante busca
- **Feedback de erro** quando visitante não encontrado

### 2. Modal de Confirmação
- **Lista de visitas ativas** do visitante encontrado
- **Informações detalhadas**: Setor, data/hora de entrada
- **Botões de ação**: Cancelar ou Confirmar finalização
- **Tratamento de casos especiais**: Visitante sem visitas ativas

### 3. Finalização Manual
- **Confirmação explícita** pelo usuário
- **Chamada à API** de finalização
- **Feedback de sucesso/erro**
- **Limpeza automática** do formulário

---

## 🔌 APIs Utilizadas

### 1. Reconhecimento Facial
**Endpoint:** `{% url 'recepcao:api_reconhecer_rosto' %}`
```javascript
// Requisição
{
    "image": "data:image/jpeg;base64,..."
}

// Resposta de sucesso
{
    "success": true,
    "visitante_id": 123,
    "nome_visitante": "João Silva"
}
```

### 2. Busca de Visitante Ativo
**Endpoint:** `{% url 'recepcao:api_buscar_visitante_ativo' %}`
```javascript
// Parâmetros
?query=João%20Silva

// Resposta
{
    "success": true,
    "visitantes": [{
        "id": 123,
        "nome": "João Silva",
        "visitas": [...]
    }]
}
```

### 3. Finalização de Visitas
**Endpoint:** `{% url 'recepcao:api_finalizar_visitas' %}`
```javascript
// Requisição
{
    "visitante_id": 123
}

// Resposta
{
    "success": true,
    "message": "2 visitas finalizadas com sucesso",
    "visitas_finalizadas": [...]
}
```

---

## ⚙️ Aspectos Técnicos

### Dependências Externas
- **MediaPipe Tasks Vision**: Face detection em tempo real
- **Bootstrap 5**: Modal e componentes UI
- **Font Awesome**: Ícones da interface

### Configurações de Câmera
```javascript
const stream = await navigator.mediaDevices.getUserMedia({
    video: { 
        width: { ideal: 1280, max: 1920 }, 
        height: { ideal: 720, max: 1080 } 
    }
});
```

### Parâmetros de Detecção
- **Face Width Percent**: 25% da largura da tela (proximidade mínima)
- **Recognition Pause**: 2000ms entre tentativas
- **Corner Length**: 20% da largura do rosto (overlay)

### Performance e Otimização
- **RequestAnimationFrame**: Loop otimizado de detecção
- **Debounce**: 500ms para busca por texto
- **Canvas Overlay**: Posicionamento absoluto sem interferir no vídeo
- **Timeout Management**: Controle de pausas entre reconhecimentos

---

## 🎛️ Estados e Controles

### Estados da Aplicação
- `isRecognitionPaused`: Pausa o reconhecimento durante processamento
- `currentVisitorId`: ID do visitante selecionado na busca manual
- `faceDetector`: Instância do detector MediaPipe

### Controle de Fluxo
- **Inicialização sequencial**: Modelo IA → Câmera → Detecção
- **Tratamento de erros**: Fallback para métodos alternativos
- **Cleanup automático**: Liberação de recursos ao sair da página

---

## 🚀 Melhorias Implementadas

### Visual
- ✅ **Design consistente** com outras páginas do totem
- ✅ **Gradientes coloridos** nos títulos
- ✅ **Separadores visuais** elegantes
- ✅ **Responsividade** para diferentes tamanhos de tela

### Funcional
- ✅ **Dual system**: Facial + Manual
- ✅ **Feedback em tempo real** para o usuário
- ✅ **Tratamento de erros** robusto
- ✅ **Navegação intuitiva** com botão voltar

### Performance
- ✅ **Otimização de requisições** com debounce
- ✅ **Loop eficiente** de detecção facial
- ✅ **Gerenciamento de estado** consistente
- ✅ **Liberação de recursos** adequada

---

## 📊 Métricas e Monitoramento

### Eventos Trackáveis
- Inicialização da câmera
- Tentativas de reconhecimento facial
- Buscas por texto realizadas
- Visitas finalizadas com sucesso
- Erros de comunicação com APIs

### Logs de Debug
- Erros de inicialização da câmera
- Falhas no reconhecimento facial  
- Respostas das APIs
- Estados de pausa/retomada do sistema

---

## 🔒 Segurança e Privacidade

### Proteção de Dados
- **CSRF Token**: Proteção contra ataques CSRF
- **Validação server-side**: Todas as requisições validadas no backend
- **Sanitização**: Input do usuário tratado adequadamente

### Câmera e Mídia
- **Permissões explícitas**: Solicitação de acesso à câmera
- **Dados locais**: Frames processados apenas no cliente
- **Sem armazenamento**: Imagens não persistidas no dispositivo

---

## 🎯 Conclusão

A página de **Finalizar Visita** representa uma evolução significativa na experiência do usuário do sistema URUTAU, oferecendo:

- **Autonomia total** para o visitante
- **Duas modalidades** de operação (facial/manual)
- **Interface intuitiva** e consistente
- **Feedback rico** em tempo real
- **Integração robusta** com o backend
- **Performance otimizada** para uso em totem

A implementação segue as melhores práticas de desenvolvimento web moderno, garantindo uma experiência fluida e confiável para os usuários do sistema. 