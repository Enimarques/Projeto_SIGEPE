import { createMediaPipeRecognitionSession } from './totem_media_pipe_recognition.js';

const config = window.TOTEM_IDENTIFICACAO_CONFIG || {};
const recognizeUrl = config.recognizeUrl;
const confirmUrl = config.confirmUrl;
const welcomeUrl = config.welcomeUrl;
const csrfToken = config.csrfToken;

if (!recognizeUrl || !confirmUrl) {
    console.error('Configurações incompletas para o totem de identificação.');
}

export async function initializeIdentificacao() {
    const video = document.getElementById('video');
    const overlay = document.getElementById('overlay');
    const statusMessage = document.getElementById('status-message');
    
    // Counter for failed recognition attempts
    let failedAttempts = 0;
    const MAX_ATTEMPTS = 3;
    
    // Recognition session variable
    let recognitionSession = null;

    function updateStatus(message, spinner = false, color = '#555') {
        statusMessage.innerHTML = `${spinner ? '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">...</span></div>' : ''} ${message}`;
        statusMessage.style.color = color;
    }

    async function sendFrameForRecognition() {
        if (!video) return;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const imageDataUrl = canvas.toDataURL('image/jpeg');

        updateStatus('🔍 Analisando seu rosto...', true, '#28a745');
        try {
            const response = await fetch(recognizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ image: imageDataUrl })
            });
            const data = await response.json();

            if (data.success && data.visitante_id) {
                updateStatus(`✅ Bem-vindo(a), ${data.nome_visitante}! Redirecionando...`, true, '#28a745');
                setTimeout(() => {
                    window.location.href = `${confirmUrl}?visitante_id=${data.visitante_id}`;
                }, 1500);
            } else {
                failedAttempts++;
                
                if (failedAttempts >= MAX_ATTEMPTS) {
                    // After 3 failed attempts, redirect to recadastro facial
                    updateStatus('🔄 Muitas tentativas sem sucesso. Redirecionando para cadastro...', true, '#28a745');
                    setTimeout(() => {
                        // Use the welcomeUrl from config and append the correct path
                        const baseUrl = welcomeUrl ? welcomeUrl.replace('/welcome/', '') : '/visitantes/recepcao/totem';
                        window.location.href = `${baseUrl}/recadastro-facial/`;
                    }, 2000);
                } else {
                    updateStatus(`🚫 Rosto não reconhecido. Tentativa ${failedAttempts}/${MAX_ATTEMPTS}. Tente novamente.`, false, '#ffc107');
                    // Resume the recognition session to allow for another attempt
                    if (recognitionSession) {
                        recognitionSession.resume();
                    }
                }
            }
        } catch (err) {
            console.error('Erro ao reconhecer rosto:', err);
            updateStatus('❌ Erro ao comunicar com o servidor. Tente novamente.', false, '#dc3545');
            // Resume the recognition session even after an error
            if (recognitionSession) {
                recognitionSession.resume();
            }
        }
    }

    function handleFaceAccepted() {
        // Pause the recognition session during processing
        if (recognitionSession) {
            recognitionSession.pause();
        }
        sendFrameForRecognition();
    }

    function handleFaceTooFar() {
        updateStatus('📏 Aproxime-se da câmera para melhorar a detecção.', false, '#ffc107');
    }

    function handleFaceLost() {
        updateStatus('👤 Posicione seu rosto na área da câmera para iniciar identificação.', false, '#6c757d');
    }

    try {
        recognitionSession = createMediaPipeRecognitionSession({
            videoElement: video,
            overlayElement: overlay,
            desiredFaceWidthPercent: 0.25,
            statusUpdater: (message, spinner, color) => updateStatus(message, spinner, color),
            onFaceAccepted: handleFaceAccepted,
            onFaceTooFar: handleFaceTooFar,
            onFaceLost: handleFaceLost,
            messages: {
                loading: '🤖 Carregando modelo de IA para reconhecimento facial...',
                camera: '📷 Iniciando câmera...',
                ready: '🎯 Sistema pronto! Posicione seu rosto.',
                prompt: '👤 Posicione seu rosto na área da câmera para iniciar identificação.'
            }
        });
        recognitionSession.start();
    } catch (err) {
        console.error('Falha ao iniciar reconhecimento facial:', err);
        updateStatus('❌ Não foi possível iniciar a câmera.', false, '#dc3545');
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeIdentificacao);
} else {
    initializeIdentificacao();
}