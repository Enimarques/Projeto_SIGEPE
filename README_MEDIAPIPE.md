# MediaPipe Tasks Vision - Instalação Local

Este documento explica como baixar e usar as bibliotecas do MediaPipe Tasks Vision localmente, em vez de depender de CDNs externos.

## 📦 Estrutura de Arquivos

Os arquivos do MediaPipe são armazenados em:
```
/opt/ProjetoSigepe/static/mediapipe/
├── vision_bundle.js          # Biblioteca principal do MediaPipe
├── wasm/                     # Arquivos WASM necessários
│   ├── vision_wasm_internal.js
│   └── vision_wasm_internal.wasm
└── models/                   # Modelos de IA
    └── blaze_face_short_range.tflite
```

## 🔽 Como Baixar os Arquivos

### Opção 1: Script Automático (Recomendado)

Execute o script de download quando tiver conexão com a internet:

```bash
cd /opt/ProjetoSigepe
bash scripts/download_mediapipe.sh
```

O script irá:
- Baixar `vision_bundle.js` (biblioteca principal)
- Baixar o modelo `blaze_face_short_range.tflite`
- Tentar baixar os arquivos WASM necessários

### Opção 2: Download Manual

Se o script não funcionar, você pode baixar manualmente:

```bash
# Criar diretórios
mkdir -p /opt/ProjetoSigepe/static/mediapipe/{wasm,models}

# Baixar biblioteca principal
cd /opt/ProjetoSigepe/static/mediapipe
wget -O vision_bundle.js \
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/vision_bundle.js"

# Baixar modelo
cd models
wget -O blaze_face_short_range.tflite \
    "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_face_short_range.tflite"
```

## 🔄 Como Funciona o Fallback

Os templates foram atualizados para:

1. **Tentar carregar arquivos locais primeiro**
2. **Fazer fallback automático para CDN** se os arquivos locais não existirem

Isso garante que o sistema continue funcionando mesmo se os arquivos locais não estiverem disponíveis.

## 📝 Templates Atualizados

Os seguintes templates foram atualizados para usar arquivos locais:

- `templates/recepcao/totem_identificacao.html`
- `templates/recepcao/totem_finalize_search.html`
- `templates/recepcao/totem_welcome.html`

## ✅ Verificação

Após baixar os arquivos, você pode verificar se estão corretos:

```bash
# Verificar tamanho dos arquivos (não devem estar vazios)
ls -lh /opt/ProjetoSigepe/static/mediapipe/vision_bundle.js
ls -lh /opt/ProjetoSigepe/static/mediapipe/models/blaze_face_short_range.tflite

# O modelo deve ter aproximadamente 224KB
# O vision_bundle.js deve ter vários MB
```

## 🐛 Troubleshooting

### Arquivos não estão sendo usados

1. Verifique se os arquivos existem e não estão vazios
2. Verifique o console do navegador para mensagens de log
3. Certifique-se de que o Django está servindo arquivos estáticos corretamente

### Erros ao carregar WASM

O MediaPipe pode precisar de arquivos WASM adicionais que são carregados dinamicamente. Se houver erros:
1. Verifique o console do navegador para ver quais arquivos estão faltando
2. Baixe os arquivos manualmente conforme necessário
3. O sistema fará fallback para CDN automaticamente

## 📚 Referências

- [MediaPipe Tasks Vision](https://developers.google.com/mediapipe/solutions/vision/face_detector)
- [Documentação do MediaPipe](https://google.github.io/mediapipe/)

