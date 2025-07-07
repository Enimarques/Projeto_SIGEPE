# Detalhes do Reconhecimento Facial

O reconhecimento facial é a tecnologia central do Modo Totem, implementado com tecnologias de ponta para máxima precisão, segurança e performance. A implementação é dividida entre o frontend (detecção com MediaPipe) e o backend (identificação com face_recognition), com sistema avançado de Anti-Spoofing para defesa contra fraudes.

## Frontend: Detecção Avançada com MediaPipe

### **Tecnologia:**
-   **MediaPipe Tasks Vision**: Biblioteca de IA do Google, construída sobre TensorFlow Lite, que oferece detecção facial de alta precisão e baixa latência.
-   **Importação via ES6 Modules**: `import { FaceDetector, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js"`
-   **Processamento Local**: Toda detecção é feita no navegador, sem enviar vídeo para o servidor.
-   **Resolução Otimizada**: 800x800px para proporção quadrada ideal.

### **Funcionalidades Implementadas:**

#### **1. Detecção em Tempo Real:**
- Loop otimizado com `requestAnimationFrame` para máxima performance (~60fps)
- Detecção de múltiplos rostos com foco no principal
- Controle de proximidade baseado em 25% da largura da tela

#### **2. Sistema Anti-Spoofing Avançado:**
```javascript
const ANTI_SPOOFING_CONFIG = {
    enabled: true,
    stabilityThreshold: 1000, // ms
    movementThreshold: 0.05,
    consecutiveDetections: 5,
    sizeVariationThreshold: 0.1,
    spoofingScoreThreshold: 0.5
};
```

**Camadas de Segurança:**
- **Análise de Estabilidade**: Monitora se o rosto permanece estável por 1 segundo
- **Detecção de Movimento Natural**: Verifica movimentos sutis e naturais
- **Análise de Detecções Consecutivas**: Requer múltiplas detecções consistentes
- **Variação de Tamanho**: Detecta mudanças suspeitas no tamanho do rosto
- **Score de Spoofing**: Calcula probabilidade de fraude (0-1)

#### **3. Overlay Visual Moderno:**
```javascript
// Design avançado com gradientes e animações
const cornerLength = Math.min(canvasWidth, canvasHeight) * 0.25;
const lineWidth = 3;
const cornerRadius = 2;

// Gradiente dinâmico
const gradient = ctx.createLinearGradient(finalCanvasX, finalCanvasY, 
                                        finalCanvasX + canvasWidth, finalCanvasY + canvasHeight);
gradient.addColorStop(0, niceColor);
gradient.addColorStop(1, niceColor + '80');
```

**Características do Overlay:**
- **Cantos arredondados**: Design moderno com raio de 2px
- **Gradiente dinâmico**: Transição suave de cores
- **Animação de pulso**: Efeito sutil nas pontas dos cantos
- **Linhas internas**: Profundidade visual com linhas tracejadas
- **Pontos de referência**: Pequenos círculos nos cantos
- **Brilho de borda**: Efeito de sombra para destaque

#### **4. Posicionamento Inteligente:**
```javascript
// Centralização automática no rosto
const VERTICAL_OFFSET_PERCENT = 0.35; // Centraliza nos olhos
const verticalOffset = -canvasHeight * VERTICAL_OFFSET_PERCENT;
finalCanvasY += verticalOffset;
```

**Sistema de Centralização:**
- **Offset vertical**: 35% para cima para centralizar nos olhos
- **Escala automática**: Adapta-se à resolução da câmera
- **Limites de canvas**: Previne overlay fora da área visível
- **Logs detalhados**: Debug completo de posicionamento

#### **5. Feedback Visual Avançado:**
-   🟡 **Amarelo**: Rosto detectado, verificando segurança
-   🟢 **Verde**: Rosto aprovado, processando identificação
-   🔴 **Vermelho**: Tentativa de fraude detectada
-   **Mensagens dinâmicas**: Sistema de status com emojis e cores

### **Processo de Detecção Atualizado:**
```javascript
async function detectFacesLoop() {
    const detections = faceDetector.detectForVideo(video, Date.now()).detections;
    
    if (detections.length > 0) {
        const face = detections[0].boundingBox;
        const keypoints = detections[0].keypoints || [];
        const faceWidthPercent = face.width / video.videoWidth;
        
        // Anti-Spoofing Analysis
        let spoofingAnalysis = { isSpoofing: false, score: 0, warnings: [] };
        
        if (ANTI_SPOOFING_CONFIG.enabled) {
            spoofingAnalysis = detectSpoofingAttempts(face, keypoints);
            
            if (spoofingAnalysis.isSpoofing) {
                drawOverlay(face, '#dc3545', keypoints, {
                    spoofingScore: spoofingAnalysis.score.toFixed(3),
                    warnings: spoofingAnalysis.warnings.join(', ')
                });
                updateStatus('🚨 Tentativa de fraude detectada!', false, '#dc3545');
                return;
            }
        }
        
        if (faceWidthPercent >= DESIRED_FACE_WIDTH_PERCENT) {
            if (!ANTI_SPOOFING_CONFIG.enabled || spoofingAnalysis.score < 0.5) {
                drawOverlay(face, '#28a745', keypoints, {
                    faceWidthPercent: faceWidthPercent,
                    spoofingScore: spoofingAnalysis.score.toFixed(3)
                });
                updateStatus('🎯 Ótimo! Analisando...', true, '#28a745');
                sendFrameForRecognition();
            } else {
                drawOverlay(face, '#ffc107', keypoints, {
                    spoofingScore: spoofingAnalysis.score.toFixed(3),
                    warnings: 'Aguardando estabilização'
                });
                updateStatus('🔒 Verificando segurança...', false, '#ffc107');
            }
        } else {
            drawOverlay(face, '#ffc107', keypoints, {
                faceWidthPercent: faceWidthPercent
            });
            updateStatus('📏 Aproxime-se da câmera', false, '#ffc107');
        }
    } else {
        drawOverlay(null);
        updateStatus('👤 Posicione seu rosto na área da câmera', false, '#6c757d');
    }
}
```

### **Configuração Otimizada:**
-   **Resolução da Câmera**: 800x800px (proporção quadrada)
-   **Modelo**: BlazeFace Short Range para detecção rápida
-   **Taxa de Atualização**: ~60fps com `requestAnimationFrame`
-   **Tolerância**: 25% da largura da tela para proximidade mínima
-   **Anti-Spoofing**: Habilitado por padrão com configurações rigorosas

## Backend: Identificação Robusta com `face_recognition`

### **Tecnologia:**
-   **face_recognition**: Biblioteca Python de alto nível baseada na poderosa `dlib` com algoritmos HOG e CNN.
-   **Vetores Biométricos**: Representação de 128 dimensões das características faciais únicas.
-   **Comparação Euclidiana**: Cálculo de distância entre vetores para determinar similaridade.

### **APIs de Reconhecimento:**

#### **1. Cadastro de Visitantes:**
```python
def save_biometric_vector(visitante, foto):
    """Gera e salva vetor biométrico durante cadastro"""
    try:
        imagem = face_recognition.load_image_file(foto)
        encodings = face_recognition.face_encodings(imagem)
        
        if encodings:
            visitante.biometric_vector = encodings[0].tolist()
            visitante.save()
            logging.info(f"Vetor biométrico gerado para {visitante.nome_completo}")
        else:
            logging.warning(f"Nenhum rosto detectado na foto de {visitante.nome_completo}")
    except Exception as e:
        logging.error(f"Erro ao gerar vetor: {e}")
```

#### **2. Reconhecimento no Totem:**
```python
def api_reconhecer_rosto(request):
    """Endpoint principal de reconhecimento facial"""
    try:
        # Decodifica imagem Base64
        image_data = request.POST.get('image')
        imagem = decode_base64_image(image_data)
        
        # Gera vetor do rosto recebido
        encodings = face_recognition.face_encodings(imagem)
        if not encodings:
            return JsonResponse({'success': False, 'error': 'Nenhum rosto detectado'})
        
        # Compara com todos os visitantes
        rosto_conhecido = encodings[0]
        visitantes = Visitante.objects.exclude(biometric_vector__isnull=True)
        
        for visitante in visitantes:
            vetor_salvo = np.array(visitante.biometric_vector)
            distancia = face_recognition.face_distance([vetor_salvo], rosto_conhecido)[0]
            
            if distancia < TOLERANCIA_RECONHECIMENTO:  # ~0.6
                logging.info(f"Visitante reconhecido: {visitante.nome_completo} (confiança: {round((1 - distancia) * 100, 2)}%)")
                return JsonResponse({
                    'success': True,
                    'visitante_id': visitante.id,
                    'nome_visitante': visitante.nome_social or visitante.nome_completo,
                    'confianca': round((1 - distancia) * 100, 2)
                })
        
        logging.warning("Visitante não reconhecido - nenhuma correspondência encontrada")
        return JsonResponse({'success': False, 'error': 'Visitante não reconhecido'})
    except Exception as e:
        logging.error(f"Erro no reconhecimento: {e}")
        return JsonResponse({'success': False, 'error': str(e)})
```

### **Funcionalidades Avançadas:**

#### **Sistema Dual de Finalização:**
1.  **Reconhecimento Facial**: Automático, mesmo processo de identificação
2.  **Busca Manual**: Por nome completo, nome social ou CPF
3.  **Finalização Automática**: Encerra todas as visitas ativas do visitante

#### **Configurações de Performance:**
-   **Tolerância**: 0.6 (ajustável para precisão vs. sensibilidade)
-   **Modelo**: HOG para speed, CNN para precisão em rostos pequenos
-   **Cache**: Vetores carregados em memória para comparação rápida
-   **Logs**: Registro detalhado de tentativas e resultados para auditoria

#### **Tratamento de Erros:**
-   **Imagem inválida**: Validação de formato e conteúdo
-   **Múltiplos rostos**: Processo apenas o maior/mais central
-   **Rosto não encontrado**: Feedback claro para reposicionamento
-   **Timeout**: Controle de tempo para evitar travamentos

## Sistema de Debug e Monitoramento

### **Logs Detalhados:**
```javascript
// Logs de posicionamento
console.log('🎯 Posicionamento do overlay:', {
    original: { originX, originY, width, height },
    canvas: { canvasX, canvasY, canvasWidth, canvasHeight },
    final: { finalCanvasX, finalCanvasY },
    verticalOffsetPixels: Math.round(-canvasHeight * VERTICAL_OFFSET_PERCENT),
    note: 'Overlay centralizado nos olhos (35% para cima)'
});

// Logs de Anti-Spoofing
console.log('🔍 Análise Anti-Spoofing:', {
    score: spoofingAnalysis.score.toFixed(3),
    isSpoofing: spoofingAnalysis.isSpoofing,
    warnings: spoofingAnalysis.warnings,
    details: spoofingAnalysis.details
});
```

### **Botão de Debug:**
- **Forçar reconhecimento**: Bypass temporário das verificações
- **Informações de segurança**: Mostra score de spoofing em tempo real
- **Logs visuais**: Debug overlay com informações técnicas
- **Modo de teste**: Desabilita Anti-Spoofing para testes

### **Métricas de Performance:**
- **Taxa de detecção**: FPS e latência
- **Precisão**: Taxa de falsos positivos/negativos
- **Segurança**: Tentativas de fraude detectadas
- **Usabilidade**: Tempo médio de reconhecimento

## Configurações de Segurança

### **Anti-Spoofing:**
- **Estabilidade mínima**: 1000ms de rosto estável
- **Movimento natural**: Detecção de micro-movimentos
- **Detecções consecutivas**: Mínimo 5 detecções consistentes
- **Variação de tamanho**: Máximo 10% de variação
- **Score de fraude**: Threshold de 0.5 (50%)

### **Reconhecimento:**
- **Tolerância**: 0.6 (60% de similaridade mínima)
- **Timeout**: 30 segundos para reconhecimento
- **Retry**: Máximo 3 tentativas consecutivas
- **Cache**: 5 minutos de cache de vetores

### **Interface:**
- **Feedback visual**: Cores e mensagens claras
- **Animações**: Suaves e não distrativas
- **Responsividade**: Adapta-se a diferentes resoluções
- **Acessibilidade**: Contraste e tamanhos adequados 