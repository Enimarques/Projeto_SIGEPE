#!/bin/bash
# Script para baixar todas as bibliotecas do MediaPipe Tasks Vision localmente
# Execute este script quando tiver conexão com a internet

set -e

BASE_DIR="/opt/ProjetoSigepe/static/mediapipe"
WASM_DIR="${BASE_DIR}/wasm"
MODELS_DIR="${BASE_DIR}/models"

echo "📦 Baixando bibliotecas do MediaPipe Tasks Vision..."

# Criar diretórios se não existirem
mkdir -p "${WASM_DIR}"
mkdir -p "${MODELS_DIR}"

# 1. Baixar vision_bundle.js (biblioteca principal)
echo "📥 Baixando vision_bundle.js..."
wget -O "${BASE_DIR}/vision_bundle.js" \
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/vision_bundle.js" || {
    echo "❌ Erro ao baixar vision_bundle.js"
    exit 1
}

# 2. Baixar modelo de detecção facial
echo "📥 Baixando modelo blaze_face_short_range.tflite..."
wget -O "${MODELS_DIR}/blaze_face_short_range.tflite" \
    "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite" || {
    echo "❌ Erro ao baixar modelo"
    exit 1
}

# 3. Baixar arquivos WASM necessários
echo "📥 Baixando arquivos WASM..."
# O MediaPipe Tasks Vision precisa de vários arquivos WASM
# Vamos baixar a versão mais recente do pacote WASM
cd "${WASM_DIR}"

# Baixar o arquivo principal do WASM (geralmente é um bundle)
wget -O "vision_wasm_internal.js" \
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm/vision_wasm_internal.js" || {
    echo "⚠️  vision_wasm_internal.js não encontrado, continuando..."
}

# Baixar o arquivo WASM binário
wget -O "vision_wasm_internal.wasm" \
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm/vision_wasm_internal.wasm" || {
    echo "⚠️  vision_wasm_internal.wasm não encontrado, continuando..."
}

# Tentar baixar outros arquivos WASM comuns
for file in "vision_wasm_internal.js.mem" "vision_wasm_internal.wasm.mem"; do
    wget -O "${file}" \
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm/${file}" 2>/dev/null || {
        echo "⚠️  ${file} não encontrado, pulando..."
    }
done

# Verificar se os arquivos principais foram baixados
if [ ! -f "${BASE_DIR}/vision_bundle.js" ] || [ ! -s "${BASE_DIR}/vision_bundle.js" ]; then
    echo "❌ Erro: vision_bundle.js não foi baixado corretamente"
    exit 1
fi

if [ ! -f "${MODELS_DIR}/blaze_face_short_range.tflite" ]; then
    echo "❌ Erro: modelo não foi baixado corretamente"
    exit 1
fi

echo "✅ Download concluído!"
echo ""
echo "📊 Arquivos baixados:"
ls -lh "${BASE_DIR}/"
ls -lh "${WASM_DIR}/" 2>/dev/null || echo "   (nenhum arquivo WASM adicional encontrado)"
ls -lh "${MODELS_DIR}/"
echo ""
echo "💡 Nota: O MediaPipe pode precisar de arquivos WASM adicionais que são carregados dinamicamente."
echo "   Se houver erros ao usar os arquivos locais, verifique o console do navegador para ver quais arquivos estão faltando."

