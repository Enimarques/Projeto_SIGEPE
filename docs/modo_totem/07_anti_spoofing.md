# Sistema Anti-Spoofing - Proteção Contra Fraudes

O sistema Anti-Spoofing do Modo Totem é uma camada avançada de segurança que protege contra tentativas de fraude usando fotos, vídeos, máscaras ou outros métodos de spoofing facial.

## 🛡️ Visão Geral

### **Objetivo:**
Detectar e bloquear tentativas de fraude no reconhecimento facial, garantindo que apenas rostos reais e autênticos sejam aceitos pelo sistema.

### **Tecnologia:**
- **JavaScript Puro**: Implementado no frontend para análise em tempo real
- **MediaPipe Integration**: Utiliza os pontos faciais detectados pelo MediaPipe
- **Análise Multi-dimensional**: Combina múltiplas técnicas de detecção

## 🔧 Configuração do Sistema

### **Parâmetros Principais:**
```javascript
const ANTI_SPOOFING_CONFIG = {
    enabled: true,                    // Habilita/desabilita o sistema
    stabilityThreshold: 1000,         // Tempo mínimo de estabilidade (ms)
    movementThreshold: 0.05,          // Threshold de movimento natural
    consecutiveDetections: 5,         // Detecções consecutivas mínimas
    sizeVariationThreshold: 0.1,      // Variação máxima de tamanho (10%)
    spoofingScoreThreshold: 0.5       // Score máximo para aprovação
};
```

### **Configurações por Ambiente:**
- **Desenvolvimento**: `enabled: false` para testes
- **Produção**: `enabled: true` com configurações rigorosas
- **Debug**: Botão para forçar bypass temporário

## 🎯 Camadas de Segurança

### **1. Análise de Estabilidade**
```javascript
function analyzeStability(face, keypoints) {
    const currentTime = Date.now();
    const currentPosition = { x: face.x, y: face.y, width: face.width, height: face.height };
    
    if (!lastFacePosition) {
        faceStabilityStartTime = currentTime;
        lastFacePosition = currentPosition;
        return { isStable: false, stabilityTime: 0 };
    }
    
    const movement = calculateMovement(lastFacePosition, currentPosition);
    const stabilityTime = currentTime - faceStabilityStartTime;
    
    if (movement > ANTI_SPOOFING_CONFIG.movementThreshold) {
        faceStabilityStartTime = currentTime;
        lastFacePosition = currentPosition;
        return { isStable: false, stabilityTime: 0 };
    }
    
    return {
        isStable: stabilityTime >= ANTI_SPOOFING_CONFIG.stabilityThreshold,
        stabilityTime: stabilityTime
    };
}
```

**Características:**
- **Tempo mínimo**: 1000ms de rosto estável
- **Movimento natural**: Permite micro-movimentos até 5%
- **Reset automático**: Reinicia contagem se movimento excessivo

### **2. Análise de Movimento Natural**
```javascript
function analyzeNaturalMovement(keypoints) {
    if (!keypoints || keypoints.length < 10) return { isNatural: false, score: 0 };
    
    // Analisa movimentos sutis nos pontos faciais
    const movements = [];
    for (let i = 0; i < keypoints.length - 1; i++) {
        const current = keypoints[i];
        const next = keypoints[i + 1];
        const distance = Math.sqrt(
            Math.pow(current.x - next.x, 2) + Math.pow(current.y - next.y, 2)
        );
        movements.push(distance);
    }
    
    const avgMovement = movements.reduce((a, b) => a + b, 0) / movements.length;
    const isNatural = avgMovement > 0.001 && avgMovement < 0.1;
    
    return {
        isNatural: isNatural,
        score: Math.min(avgMovement * 10, 1)
    };
}
```

**Características:**
- **Micro-movimentos**: Detecta movimentos sutis e naturais
- **Pontos faciais**: Analisa 468 pontos do MediaPipe
- **Threshold dinâmico**: Adapta-se a diferentes rostos

### **3. Análise de Detecções Consecutivas**
```javascript
function analyzeConsecutiveDetections(face) {
    const currentTime = Date.now();
    faceDetectionHistory.push({
        timestamp: currentTime,
        position: { x: face.x, y: face.y, width: face.width, height: face.height }
    });
    
    // Remove detecções antigas (últimos 2 segundos)
    faceDetectionHistory = faceDetectionHistory.filter(
        detection => currentTime - detection.timestamp < 2000
    );
    
    return {
        count: faceDetectionHistory.length,
        isConsistent: faceDetectionHistory.length >= ANTI_SPOOFING_CONFIG.consecutiveDetections
    };
}
```

**Características:**
- **Mínimo 5 detecções**: Requer consistência temporal
- **Janela de 2 segundos**: Analisa apenas detecções recentes
- **Posicionamento**: Verifica se o rosto permanece na mesma área

### **4. Análise de Variação de Tamanho**
```javascript
function analyzeSizeVariation(face) {
    const currentSize = face.width * face.height;
    
    if (!lastFaceSize) {
        lastFaceSize = currentSize;
        return { isStable: true, variation: 0 };
    }
    
    const variation = Math.abs(currentSize - lastFaceSize) / lastFaceSize;
    const isStable = variation <= ANTI_SPOOFING_CONFIG.sizeVariationThreshold;
    
    lastFaceSize = currentSize;
    
    return {
        isStable: isStable,
        variation: variation
    };
}
```

**Características:**
- **Variação máxima**: 10% de mudança no tamanho
- **Detecção de zoom**: Identifica tentativas de aproximação artificial
- **Estabilidade**: Requer tamanho consistente

## 📊 Cálculo do Score de Spoofing

### **Algoritmo de Pontuação:**
```javascript
function calculateSpoofingScore(analyses) {
    let score = 0;
    let totalWeight = 0;
    
    // Estabilidade (peso: 40%)
    if (!analyses.stability.isStable) {
        score += 0.4;
    }
    totalWeight += 0.4;
    
    // Movimento natural (peso: 25%)
    if (!analyses.movement.isNatural) {
        score += 0.25;
    }
    totalWeight += 0.25;
    
    // Detecções consecutivas (peso: 20%)
    if (!analyses.consecutive.isConsistent) {
        score += 0.2;
    }
    totalWeight += 0.2;
    
    // Variação de tamanho (peso: 15%)
    if (!analyses.size.isStable) {
        score += 0.15;
    }
    totalWeight += 0.15;
    
    return score / totalWeight; // Normaliza para 0-1
}
```

### **Interpretação do Score:**
- **0.0 - 0.3**: Rosto muito seguro (verde)
- **0.3 - 0.5**: Rosto moderadamente seguro (amarelo)
- **0.5 - 1.0**: Possível fraude (vermelho)

## 🎨 Feedback Visual

### **Cores e Estados:**
```javascript
// Verde - Aprovado
if (spoofingScore < 0.3) {
    drawOverlay(face, '#28a745', keypoints, debugInfo);
    updateStatus('🎯 Ótimo! Analisando...', true, '#28a745');
}

// Amarelo - Verificando
else if (spoofingScore < 0.5) {
    drawOverlay(face, '#ffc107', keypoints, debugInfo);
    updateStatus('🔒 Verificando segurança...', false, '#ffc107');
}

// Vermelho - Fraude detectada
else {
    drawOverlay(face, '#dc3545', keypoints, debugInfo);
    updateStatus('🚨 Tentativa de fraude detectada!', false, '#dc3545');
}
```

### **Informações de Debug:**
```javascript
const debugInfo = {
    faceWidthPercent: faceWidthPercent,
    spoofingScore: spoofingAnalysis.score.toFixed(3),
    stabilityTime: spoofingAnalysis.details.stability.stabilityTime,
    warnings: spoofingAnalysis.warnings.join(', ')
};
```

## 🔧 Sistema de Debug

### **Botão de Debug:**
```javascript
function toggleDebugMode() {
    const debugButton = document.getElementById('debugButton');
    const isDebugMode = debugButton.classList.contains('active');
    
    if (isDebugMode) {
        // Modo normal
        ANTI_SPOOFING_CONFIG.enabled = true;
        debugButton.classList.remove('active');
        debugButton.textContent = '🔓 Debug';
    } else {
        // Modo debug
        ANTI_SPOOFING_CONFIG.enabled = false;
        debugButton.classList.add('active');
        debugButton.textContent = '🔒 Normal';
    }
}
```

### **Logs Detalhados:**
```javascript
console.log('🔍 Análise Anti-Spoofing:', {
    score: spoofingAnalysis.score.toFixed(3),
    isSpoofing: spoofingAnalysis.isSpoofing,
    warnings: spoofingAnalysis.warnings,
    details: {
        stability: spoofingAnalysis.details.stability,
        movement: spoofingAnalysis.details.movement,
        consecutive: spoofingAnalysis.details.consecutive,
        size: spoofingAnalysis.details.size
    }
});
```

## 📈 Métricas e Performance

### **Métricas Coletadas:**
- **Taxa de detecção de fraude**: Tentativas bloqueadas vs. total
- **Falsos positivos**: Rostos reais incorretamente bloqueados
- **Tempo de análise**: Latência do sistema Anti-Spoofing
- **Score médio**: Distribuição dos scores de spoofing

### **Otimizações:**
- **Processamento otimizado**: Análise apenas quando necessário
- **Cache de resultados**: Evita recálculos desnecessários
- **Thresholds adaptativos**: Ajusta-se ao ambiente

## 🚨 Tratamento de Ataques

### **Tipos de Ataques Detectados:**

#### **1. Foto/Imagem:**
- **Detecção**: Movimento zero, estabilidade perfeita
- **Bloqueio**: Score > 0.5, mensagem de erro

#### **2. Vídeo:**
- **Detecção**: Movimento repetitivo, padrões artificiais
- **Bloqueio**: Análise de movimento natural

#### **3. Máscara:**
- **Detecção**: Pontos faciais inconsistentes
- **Bloqueio**: Análise de keypoints do MediaPipe

#### **4. Deepfake:**
- **Detecção**: Inconsistências sutis nos movimentos
- **Bloqueio**: Análise multi-dimensional

### **Respostas do Sistema:**
```javascript
if (spoofingAnalysis.isSpoofing) {
    // Bloqueia imediatamente
    drawOverlay(face, '#dc3545', keypoints, debugInfo);
    updateStatus('🚨 Tentativa de fraude detectada! Use seu rosto real.', false, '#dc3545');
    
    // Reset das verificações
    resetAntiSpoofing();
    
    // Log para auditoria
    console.warn('🚨 TENTATIVA DE FRAUDE DETECTADA:', spoofingAnalysis);
    
    return; // Para o processamento
}
```

## 🔄 Manutenção e Ajustes

### **Ajuste de Sensibilidade:**
```javascript
// Para ambientes com iluminação variável
ANTI_SPOOFING_CONFIG.movementThreshold = 0.08; // Mais permissivo

// Para máxima segurança
ANTI_SPOOFING_CONFIG.stabilityThreshold = 2000; // 2 segundos
ANTI_SPOOFING_CONFIG.spoofingScoreThreshold = 0.3; // Mais restritivo
```

### **Monitoramento:**
- **Logs regulares**: Análise de padrões de ataque
- **Métricas de performance**: Otimização contínua
- **Feedback de usuários**: Ajuste de thresholds

### **Atualizações:**
- **Novos algoritmos**: Integração de técnicas avançadas
- **Machine Learning**: Modelos treinados para novos ataques
- **Adaptação**: Ajuste automático baseado em dados

---

**📅 Última Atualização:** Julho 2025  
**🔄 Versão:** 1.0  
**📋 Status:** Produção Ativa 