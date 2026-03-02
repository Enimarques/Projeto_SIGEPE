import { createMediaPipeRecognitionSession } from './totem_media_pipe_recognition.js';

const config = window.TOTEM_RECADASTRO_CONFIG || {};
const validateCpfUrl = config.validateCpfUrl;
const reenrollUrl = config.reenrollUrl;
const destinationUrl = config.destinationUrl;
const csrfToken = config.csrfToken;

if (!validateCpfUrl || !reenrollUrl) {
    console.error('Configurações incompletas para o recadastro facial.');
}

document.addEventListener('DOMContentLoaded', () => {
    const cpfInput = document.getElementById('cpf-input');
    const cpfError = document.getElementById('cpf-error');
    const numpadButtons = document.querySelectorAll('.numpad button');
    const stepCpf = document.getElementById('step-cpf');
    const stepFace = document.getElementById('step-face');
    const statusFace = document.getElementById('status-face');
    const videoFace = document.getElementById('video-face');
    const overlayFace = document.getElementById('overlay-face');

    let visitanteId = null;
    let recognitionSession = null;
    let processingCapture = false;

    const formatInfo = {
        currency: { style: 'currency', currency: 'BRL' }
    };

    function onlyDigits(value) {
        return value.replace(/\D/g, '');
    }

    function formatCpf(value) {
        const digits = onlyDigits(value).slice(0, 11);
        let v = digits;
        if (v.length > 3 && v.length <= 6) v = v.replace(/(\d{3})(\d+)/, '$1.$2');
        else if (v.length > 6 && v.length <= 9) v = v.replace(/(\d{3})(\d{3})(\d+)/, '$1.$2.$3');
        else if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
        return v;
    }

    function updateCpfInput(newValue) {
        cpfInput.value = formatCpf(newValue);
    }

    function handleNumpadClick(key) {
        cpfError.textContent = '';
        const currentDigits = onlyDigits(cpfInput.value);
        if (key === 'back') {
            updateCpfInput(currentDigits.slice(0, -1));
        } else if (key === 'ok') {
            validateCpf();
        } else if (currentDigits.length < 11) {
            updateCpfInput(currentDigits + key);
        }
    }

    numpadButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            handleNumpadClick(btn.getAttribute('data-key'));
        });
    });

    async function validateCpf() {
        const digits = onlyDigits(cpfInput.value);
        if (digits.length !== 11) {
            cpfError.textContent = 'CPF inválido. Verifique os números digitados.';
            return;
        }
        try {
            cpfError.textContent = 'Validando CPF...';
            const response = await fetch(validateCpfUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ cpf: cpfInput.value })
            });
            const data = await response.json();
            if (response.status === 404 || data.error === 'CPF_NOT_FOUND') {
                cpfError.textContent = 'CPF não localizado. Procure a recepção.';
                return;
            }
            if (!data.success) {
                cpfError.textContent = data.error || 'Erro ao validar CPF.';
                return;
            }
            visitanteId = data.visitante_id;
            stepCpf.style.display = 'none';
            stepFace.style.display = 'block';
            startFaceRecognition();
        } catch (e) {
            cpfError.textContent = 'Erro de comunicação. Tente novamente.';
        }
    }

    function updateFaceStatus(message, color = '#6c757d') {
        statusFace.textContent = message;
        statusFace.style.color = color;
    }

    async function captureFrameAndSend() {
        if (!videoFace || !visitanteId) return;
        const canvas = document.createElement('canvas');
        canvas.width = videoFace.videoWidth;
        canvas.height = videoFace.videoHeight;
        canvas.getContext('2d').drawImage(videoFace, 0, 0);
        const imageDataUrl = canvas.toDataURL('image/jpeg');

        updateFaceStatus('📸 Capturando nova foto...', '#28a745');
        try {
            const response = await fetch(reenrollUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ image: imageDataUrl, visitante_id: visitanteId })
            });
            const data = await response.json();
            if (data.success && data.visitante_id) {
                updateFaceStatus('✅ Foto atualizada com sucesso! Redirecionando...', '#28a745');
                recognitionSession?.stop();
                setTimeout(() => {
                    window.location.href = `${destinationUrl}?visitante_id=${data.visitante_id}`;
                }, 1500);
            } else {
                updateFaceStatus(data.error || '😕 Nenhum rosto detectado. Ajuste sua posição e aguarde.', '#ffc107');
                recognitionSession?.resume();
            }
        } catch (e) {
            console.error('Erro ao enviar imagem:', e);
            updateFaceStatus('❌ Erro ao enviar a imagem. Tentando novamente...', '#dc3545');
            recognitionSession?.resume();
        }
    }

    function handleFaceAccepted() {
        if (processingCapture) return;
        processingCapture = true;
        recognitionSession?.pause();
        captureFrameAndSend().finally(() => {
            processingCapture = false;
        });
    }

    function handleFaceTooFar() {
        if (!processingCapture) {
            updateFaceStatus('📏 Aproxime-se para ajustar o tamanho do rosto.', '#ffc107');
        }
    }

    function handleFaceLost() {
        if (!processingCapture) {
            updateFaceStatus('👤 Posicione seu rosto no centro da câmera.', '#6c757d');
        }
    }

    function startFaceRecognition() {
        updateFaceStatus('🤖 Iniciando câmera...', '#6c757d');
        try {
            recognitionSession = createMediaPipeRecognitionSession({
                videoElement: videoFace,
                overlayElement: overlayFace,
                desiredFaceWidthPercent: 0.25,
                statusUpdater: (message, spinner, color) => updateFaceStatus(message, color),
                onFaceAccepted: handleFaceAccepted,
                onFaceTooFar: handleFaceTooFar,
                onFaceLost: handleFaceLost,
                messages: {
                    loading: '🤖 Carregando modelo de IA...',
                    camera: '📹 Iniciando câmera...',
                    ready: '🎯 Sistema pronto! Centralize seu rosto.',
                    prompt: '👤 Posicione seu rosto no centro da câmera.'
                }
            });
            recognitionSession.start();
        } catch (error) {
            console.error('Erro ao iniciar a câmera:', error);
            updateFaceStatus('❌ Não foi possível acessar a câmera. Procure a recepção.', '#dc3545');
        }
    }
});
