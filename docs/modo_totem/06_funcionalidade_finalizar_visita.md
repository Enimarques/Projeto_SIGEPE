# Funcionalidade de Finalizar Visita

A funcionalidade de **Finalizar Visita** representa uma evolução significativa do sistema URUTAU, permitindo que visitantes encerrem suas visitas de forma autônoma através do totem, sem necessidade de intervenção da recepção.

## Visão Geral

**URL:** `http://127.0.0.1:8000/recepcao/totem/finalize_search/`  
**Template:** `templates/recepcao/totem_finalize_search.html`  
**View:** `apps.recepcao.views.totem_finalize_search`

### **Características Principais:**
- 🎯 **Sistema Dual**: Reconhecimento facial + Busca manual
- 🤖 **IA Avançada**: MediaPipe para detecção em tempo real
- 📱 **Interface Responsiva**: Design consistente com todo o sistema
- ⚡ **Performance Otimizada**: Debounce, timeouts e cache inteligente
- 🔒 **Segurança**: Validação robusta e proteção CSRF

---

## Modalidades de Finalização

### 1. 🎥 Reconhecimento Facial Automático

#### **Tecnologia:**
- **MediaPipe Tasks Vision**: Detecção facial de alta precisão
- **Canvas Overlay**: Feedback visual com cantos coloridos
- **RequestAnimationFrame**: Loop otimizado para máxima performance

#### **Fluxo de Uso:**
1. **Inicialização**: Carregamento do modelo IA e configuração da câmera
2. **Detecção**: Sistema localiza rosto e avalia proximidade
3. **Feedback Visual**: 
   - 🟡 Amarelo: Aproximar mais
   - 🟢 Verde: Posição ideal, analisando
4. **Reconhecimento**: Identifica visitante via comparação biométrica
5. **Finalização**: Encerra todas as visitas ativas automaticamente
6. **Confirmação**: Exibe sucesso e redireciona

#### **Mensagens de Status:**
```javascript
// Exemplos de feedback em tempo real
"Carregando modelo de IA para reconhecimento facial..."
"Iniciando câmera e configurando detecção..."
"Posicione seu rosto na câmera para finalizar visita"
"Aproxime-se um pouco mais da câmera"
"Ótimo! Analisando rosto para finalizar visita..."
"Reconhecido: João Silva! Finalizando visitas..."
"✅ Visitas de João Silva finalizadas com sucesso!"
```

### 2. ⌨️ Busca Manual por Texto

#### **Funcionalidades:**
- **Busca Dinâmica**: Resultados em tempo real com debounce de 500ms
- **Múltiplos Campos**: Nome completo, nome social, CPF
- **Validação**: Mínimo de 3 caracteres para iniciar busca
- **Modal de Confirmação**: Lista detalhada das visitas ativas

#### **Fluxo de Uso:**
1. **Digitação**: Usuário digita nome ou CPF
2. **Busca Automática**: Sistema procura visitantes com visitas ativas
3. **Seleção**: Modal exibe visitante encontrado e suas visitas
4. **Confirmação**: Lista detalhada com setor e horário de entrada
5. **Finalização**: Encerra todas as visitas com confirmação explícita

#### **Tratamento de Casos:**
- **Visitante não encontrado**: Mensagem clara de erro
- **Sem visitas ativas**: Informa que não há visitas para finalizar
- **Múltiplas visitas**: Lista todas para confirmação do usuário

---

## Implementação Técnica

### **Frontend - JavaScript ES6+**

#### **Reconhecimento Facial:**
```javascript
import { FaceDetector, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

async function initializeFaceRecognition() {
    // Carrega modelo MediaPipe
    const filesetResolver = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
    );
    
    faceDetector = await FaceDetector.createFromOptions(filesetResolver, {
        baseOptions: { 
            modelAssetPath: "storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite" 
        },
        runningMode: 'VIDEO'
    });
    
    // Configura câmera e inicia detecção
    const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280, max: 1920 }, height: { ideal: 720, max: 1080 } }
    });
    
    video.srcObject = stream;
    detectFacesLoop();
}

async function detectFacesLoop() {
    const detections = faceDetector.detectForVideo(video, Date.now()).detections;
    
    if (detections.length > 0) {
        const face = detections[0].boundingBox;
        const faceWidthPercent = face.width / video.videoWidth;
        
        if (faceWidthPercent >= 0.25) {
            drawOverlay(face, '#28a745');
            sendFrameForRecognition();
        } else {
            drawOverlay(face, '#ffc107');
        }
    }
    
    requestAnimationFrame(detectFacesLoop);
}
```

#### **Busca por Texto:**
```javascript
// Debounce para otimizar requisições
let searchTimeout;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchVisitor(searchInput.value);
    }, 500);
});

async function searchVisitor(query) {
    if (query.length < 3) return;
    
    const response = await fetch(
        `/recepcao/api/buscar-visitante-ativo/?query=${encodeURIComponent(query)}`
    );
    const data = await response.json();
    
    if (data.success && data.visitantes.length > 0) {
        showVisitorModal(data.visitantes[0]);
    }
}
```

### **Backend - Django Views**

#### **API de Finalização:**
```python
def api_finalizar_visitas(request):
    """Finaliza todas as visitas ativas de um visitante"""
    try:
        data = json.loads(request.body)
        visitante_id = data.get('visitante_id')
        
        # Busca visitas ativas
        visitas_ativas = Visita.objects.filter(
            visitante_id=visitante_id,
            data_saida__isnull=True
        )
        
        if not visitas_ativas.exists():
            return JsonResponse({
                'success': False, 
                'error': 'Nenhuma visita ativa encontrada'
            })
        
        # Finaliza todas as visitas
        count = 0
        for visita in visitas_ativas:
            visita.data_saida = timezone.now()
            visita.status = 'finalizada'
            visita.save()
            count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'{count} visita(s) finalizada(s) com sucesso',
            'visitas_finalizadas': count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        })
```

#### **API de Busca:**
```python
def api_buscar_visitante_ativo(request):
    """Busca visitante com visitas ativas"""
    query = request.GET.get('query', '').strip()
    
    if len(query) < 3:
        return JsonResponse({
            'success': False,
            'error': 'Query muito curta'
        })
    
    # Busca em múltiplos campos
    visitantes = Visitante.objects.filter(
        Q(nome_completo__icontains=query) |
        Q(nome_social__icontains=query) |
        Q(cpf__icontains=query)
    ).distinct()
    
    # Filtra apenas com visitas ativas
    resultado = []
    for visitante in visitantes:
        visitas_ativas = visitante.visita_set.filter(data_saida__isnull=True)
        if visitas_ativas.exists():
            resultado.append({
                'id': visitante.id,
                'nome': visitante.nome_social or visitante.nome_completo,
                'visitas': [{
                    'setor': visita.setor.nome,
                    'data_entrada': visita.data_entrada.strftime('%d/%m/%Y %H:%M')
                } for visita in visitas_ativas]
            })
    
    return JsonResponse({
        'success': True,
        'visitantes': resultado
    })
```

---

## Design e Interface

### **Estilo Visual Consistente:**
```css
.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(45deg, #5e72e4, #825ee4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.camera-viewfinder {
    width: 640px;
    height: 480px;
    border-radius: 15px;
    background-color: #000;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border: 3px solid #fff;
}

#overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;
}
```

### **Responsividade:**
- **Desktop**: Layout full-width com elementos centralizados
- **Tablet**: Ajuste de tamanhos e espaçamentos
- **Mobile**: Stack vertical com controles touch-friendly

---

## Benefícios Implementados

### **Para Visitantes:**
- ✅ **Autonomia Total**: Finalização sem dependência da recepção
- ✅ **Múltiplas Opções**: Facial ou manual conforme preferência
- ✅ **Feedback Rico**: Orientação clara em cada etapa
- ✅ **Rapidez**: Processo otimizado para poucos segundos

### **Para Instituição:**
- ✅ **Redução de Carga**: Menos demanda na recepção
- ✅ **Dados Precisos**: Horários de saída registrados automaticamente
- ✅ **Auditoria**: Log completo de todas as finalizações
- ✅ **Experiência Moderna**: Tecnologia de ponta para visitantes

### **Para Sistema:**
- ✅ **Performance**: Otimizações de frontend e backend
- ✅ **Segurança**: Validações e proteções robustas
- ✅ **Manutenibilidade**: Código modular e bem documentado
- ✅ **Escalabilidade**: Preparado para grandes volumes

---

## Métricas e Monitoramento

### **KPIs Trackáveis:**
- Taxa de sucesso por modalidade (facial vs. manual)
- Tempo médio de finalização
- Tentativas de reconhecimento facial
- Buscas manuais realizadas
- Erros e timeouts

### **Logs de Auditoria:**
- Timestamp de cada finalização
- Método utilizado (facial/manual)
- Quantidade de visitas encerradas
- Dados do visitante (anonimizados para LGPD)
- Possíveis erros ou falhas

---

## Conclusão

A funcionalidade de **Finalizar Visita** representa um avanço tecnológico significativo no sistema URUTAU, oferecendo uma experiência moderna, autônoma e eficiente para os visitantes, enquanto reduz a carga operacional da recepção e mantém registros precisos para auditoria.

A implementação com MediaPipe, APIs REST robustas e interface responsiva garante uma solução de ponta, preparada para as demandas futuras da instituição. 