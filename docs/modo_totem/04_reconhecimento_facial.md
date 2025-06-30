# Detalhes do Reconhecimento Facial

O reconhecimento facial é a tecnologia central do Modo Totem, implementado com tecnologias de ponta para máxima precisão e performance. A implementação é dividida entre o frontend (detecção com MediaPipe) e o backend (identificação com face_recognition).

## Frontend: Detecção Avançada com MediaPipe

### **Tecnologia:**
-   **MediaPipe Tasks Vision**: Biblioteca de IA do Google, construída sobre TensorFlow Lite, que oferece detecção facial de alta precisão e baixa latência.
-   **Importação via ES6 Modules**: `import { FaceDetector, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js"`
-   **Processamento Local**: Toda detecção é feita no navegador, sem enviar vídeo para o servidor.

### **Funcionalidades Implementadas:**
1.  **Detecção em Tempo Real**: Loop otimizado com `requestAnimationFrame` para máxima performance.
2.  **Feedback Visual Avançado**: 
    -   🟡 **Amarelo**: Rosto detectado, precisa aproximar
    -   🟢 **Verde**: Rosto na posição ideal, processando
    -   **Canvas Overlay**: Cantos coloridos desenhados ao redor do rosto
3.  **Controle de Proximidade**: Calcula se o rosto ocupa pelo menos 25% da largura da tela.
4.  **Mensagens Dinâmicas**: Sistema de status com emojis e cores para guiar o usuário.

### **Processo de Detecção:**
```javascript
async function detectFacesLoop() {
    const detections = faceDetector.detectForVideo(video, Date.now()).detections;
    
    if (detections.length > 0) {
        const face = detections[0].boundingBox;
        const faceWidthPercent = face.width / video.videoWidth;
        
        if (faceWidthPercent >= DESIRED_FACE_WIDTH_PERCENT) {
            drawOverlay(face, '#28a745'); // Verde
            updateStatus('🎯 Ótimo! Analisando...', true, '#28a745');
            sendFrameForRecognition();
        } else {
            drawOverlay(face, '#ffc107'); // Amarelo
            updateStatus('📏 Aproxime-se mais...', false, '#ffc107');
        }
    }
}
```

### **Configuração Otimizada:**
-   **Resolução da Câmera**: 1280x720 (ideal) até 1920x1080 (máximo)
-   **Modelo**: BlazeFace Short Range para detecção rápida em curta distância
-   **Taxa de Atualização**: ~60fps com `requestAnimationFrame`
-   **Tolerância**: 25% da largura da tela para proximidade mínima

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
                return JsonResponse({
                    'success': True,
                    'visitante_id': visitante.id,
                    'nome_visitante': visitante.nome_social or visitante.nome_completo,
                    'confianca': round((1 - distancia) * 100, 2)
                })
        
        return JsonResponse({'success': False, 'error': 'Visitante não reconhecido'})
    except Exception as e:
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