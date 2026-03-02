import { createMediaPipeRecognitionSession } from './totem_media_pipe_recognition.js';

const config = window.TOTEM_FINALIZE_CONFIG || {};
const recognizeUrl = config.recognizeUrl;
const finalizeUrl = config.finalizeUrl;
const searchVisitorUrl = config.searchVisitorUrl;
const welcomeUrl = config.welcomeUrl;
const csrfToken = config.csrfToken;

if (!recognizeUrl || !finalizeUrl || !searchVisitorUrl) {
    console.error('Configurações do reconhecimento facial incompletas para finalize_search.');
}

const RECOGNITION_PAUSE_MS = 2000;

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const overlay = document.getElementById('overlay');
    const cameraStatus = document.getElementById('camera-status');
    const searchInput = document.getElementById('searchInput');
    const searchSpinner = document.getElementById('searchSpinner');
    const searchStatus = document.getElementById('search-status');
    const finalizeModal = new bootstrap.Modal(document.getElementById('finalizeVisitModal'));
    const visitorNameSpan = document.getElementById('visitorName');
    const visitListUl = document.getElementById('visitList');
    const noVisitsMessageDiv = document.getElementById('noVisitsMessage');
    const confirmFinalizeBtn = document.getElementById('confirmFinalizeBtn');

    const statusSpinnerHtml = `<div class="spinner-border text-primary" role="status"><span class="visually-hidden">...</span></div>`;
    const cpfNumpad = document.getElementById('cpfNumpad');
    const searchArea = document.querySelector('.search-area');
    let onlyDigitsMode = false;

    let recognitionSession = null;
    let processingRecognition = false;
    let currentVisitorId = null;
    let searchTimeout;

    function updateCameraStatus(message, spinner = false, color = '#555') {
        cameraStatus.innerHTML = `${spinner ? statusSpinnerHtml : ''} ${message}`;
        cameraStatus.style.color = color;
    }

    function scheduleRecognitionRetry() {
        setTimeout(() => {
            processingRecognition = false;
            recognitionSession?.resume();
        }, RECOGNITION_PAUSE_MS);
    }

    async function sendFrameForRecognition() {
        if (!video || !recognitionSession) return;

        try {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const imageDataUrl = canvas.toDataURL('image/jpeg');

            updateCameraStatus('Processando rosto para reconhecimento...', true, '#28a745');
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
                updateCameraStatus(`Reconhecido: ${data.nome_visitante}! Finalizando visitas...`, true, '#28a745');
                await finalizeVisitsByFaceRecognition(data.visitante_id, data.nome_visitante);
            } else {
                updateCameraStatus('Rosto não reconhecido. Tente novamente ou use busca por nome.', false, '#ffc107');
                scheduleRecognitionRetry();
            }
        } catch (error) {
            console.error('Erro ao reconhecer rosto:', error);
            updateCameraStatus('Erro de comunicação. Tentando novamente...', false, '#dc3545');
            scheduleRecognitionRetry();
        }
    }

    async function finalizeVisitsByFaceRecognition(visitanteId, nomeVisitante) {
        try {
            const response = await fetch(finalizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ visitante_id: visitanteId })
            });
            const data = await response.json();

            if (data.success) {
                updateCameraStatus(`✅ Visitas de ${nomeVisitante} finalizadas com sucesso!`, true, '#28a745');
                setTimeout(() => {
                    updateCameraStatus(`✅ ${data.message}\n\nRedirecionando para o início...`, true, '#28a745');
                    setTimeout(() => {
                        window.location.href = welcomeUrl;
                    }, 3000);
                }, 2000);
            } else {
                updateCameraStatus(`Erro: ${data.error}`, false, '#dc3545');
                scheduleRecognitionRetry();
            }
        } catch (error) {
            console.error('Erro ao finalizar visitas:', error);
            updateCameraStatus('Erro ao finalizar visitas. Tente novamente.', false, '#dc3545');
            scheduleRecognitionRetry();
        } finally {
            processingRecognition = false;
        }
    }

    function updateCameraStatus(message, spinner = false, color = '#555') {
        cameraStatus.innerHTML = `${spinner ? statusSpinnerHtml : ''} ${message}`;
        cameraStatus.style.color = color;
    }

    function scheduleRecognitionRetry() {
        setTimeout(() => {
            processingRecognition = false;
            recognitionSession?.resume();
        }, RECOGNITION_PAUSE_MS);
    }

    async function sendFrameForRecognition() {
        if (!video || !recognitionSession) return;

        try {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const imageDataUrl = canvas.toDataURL('image/jpeg');

            updateCameraStatus('Processando rosto para reconhecimento...', true, '#28a745');
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
                updateCameraStatus(`Reconhecido: ${data.nome_visitante}! Finalizando visitas...`, true, '#28a745');
                await finalizeVisitsByFaceRecognition(data.visitante_id, data.nome_visitante);
            } else {
                updateCameraStatus('Rosto não reconhecido. Tente novamente ou use busca por nome.', false, '#ffc107');
                scheduleRecognitionRetry();
            }
        } catch (error) {
            console.error('Erro ao reconhecer rosto:', error);
            updateCameraStatus('Erro de comunicação. Tentando novamente...', false, '#dc3545');
            scheduleRecognitionRetry();
        }
    }

    async function finalizeVisitsByFaceRecognition(visitanteId, nomeVisitante) {
        try {
            const response = await fetch(finalizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ visitante_id: visitanteId })
            });
            const data = await response.json();

            if (data.success) {
                updateCameraStatus(`✅ Visitas de ${nomeVisitante} finalizadas com sucesso!`, true, '#28a745');
                setTimeout(() => {
                    updateCameraStatus(`✅ ${data.message}\n\nRedirecionando para o início...`, true, '#28a745');
                    setTimeout(() => {
                        window.location.href = welcomeUrl;
                    }, 3000);
                }, 2000);
            } else {
                updateCameraStatus(`Erro: ${data.error}`, false, '#dc3545');
                scheduleRecognitionRetry();
            }
        } catch (error) {
            console.error('Erro ao finalizar visitas:', error);
            updateCameraStatus('Erro ao finalizar visitas. Tente novamente.', false, '#dc3545');
            scheduleRecognitionRetry();
        } finally {
            processingRecognition = false;
        }
    }

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

    function updateSearchInput(value) {
        searchInput.value = onlyDigitsMode ? formatCpf(value) : value;
    }

    function handleNumpadInput(key) {
        let digits = onlyDigits(searchInput.value);
        if (key === 'back') {
            digits = digits.slice(0, -1);
        } else if (key === 'ok') {
            if (digits.length >= 3) {
                searchVisitor(digits);
            }
            return;
        } else if (digits.length < 11) {
            digits += key;
        }
        updateSearchInput(digits);
    }

    function showNumpad() {
        onlyDigitsMode = true;
        if (!cpfNumpad?.classList.contains('visible')) {
            cpfNumpad?.classList.add('visible');
        }
    }

    function hideNumpad() {
        onlyDigitsMode = false;
        cpfNumpad?.classList.remove('visible');
    }

    document.addEventListener('mousedown', (event) => {
        if (!searchArea?.contains(event.target)) {
            hideNumpad();
        } else if (cpfNumpad?.contains(event.target)) {
            searchInput.focus();
        }
    });

    ['focus', 'click', 'touchstart'].forEach(eventType => {
        searchInput.addEventListener(eventType, showNumpad);
    });

    ['click', 'touchstart', 'pointerdown'].forEach(eventType => {
        searchArea?.addEventListener(eventType, () => {
            showNumpad();
            searchInput.focus();
        });
    });

    searchInput.addEventListener('blur', () => {
        setTimeout(() => {
            if (!cpfNumpad?.contains(document.activeElement)) {
                hideNumpad();
            }
        }, 100);
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            hideNumpad();
            searchInput.blur();
        }
    });

    cpfNumpad?.addEventListener('click', (event) => {
        const button = event.target.closest('button[data-key]');
        if (!button) return;

        event.preventDefault();
        handleNumpadInput(button.dataset.key);
        searchInput.focus();
    });

    async function searchVisitor(query) {
        if (!query || query.length < 3) {
            searchStatus.textContent = '';
            return;
        }

        searchSpinner.style.display = 'block';
        searchStatus.textContent = '';

        try {
            const response = await fetch(`${searchVisitorUrl}?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (response.ok && data.success && data.visitantes.length > 0) {
                const visitor = data.visitantes[0];
                currentVisitorId = visitor.id;
                visitorNameSpan.textContent = visitor.nome;
                visitListUl.innerHTML = '';

                if (visitor.visitas.length > 0) {
                    visitor.visitas.forEach(visita => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';
                        li.textContent = `Visita ao ${visita.setor} - Entrada: ${visita.data_entrada}`;
                        visitListUl.appendChild(li);
                    });
                    visitListUl.style.display = 'block';
                    noVisitsMessageDiv.style.display = 'none';
                    confirmFinalizeBtn.style.display = 'block';
                } else {
                    visitListUl.style.display = 'none';
                    noVisitsMessageDiv.innerHTML = `<strong>${visitor.nome}</strong> foi encontrado, mas não possui visitas em andamento.`;
                    noVisitsMessageDiv.style.display = 'block';
                    confirmFinalizeBtn.style.display = 'none';
                }
                finalizeModal.show();
            } else {
                searchStatus.textContent = data.error || 'Nenhum visitante com visitas em andamento encontrado.';
            }
        } catch (error) {
            searchStatus.textContent = 'Erro de comunicação com o servidor.';
            console.error('Erro ao buscar visitante:', error);
        } finally {
            searchSpinner.style.display = 'none';
        }
    }

    async function finalizeVisits() {
        if (!currentVisitorId) return;

        try {
            const response = await fetch(finalizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ visitante_id: currentVisitorId })
            });
            const data = await response.json();

            finalizeModal.hide();
            if (data.success) {
                searchStatus.textContent = `✅ ${data.message}`;
                searchStatus.style.color = '#28a745';
                searchStatus.style.fontWeight = '600';
                searchInput.value = '';
                setTimeout(() => {
                    window.location.href = welcomeUrl;
                }, 3000);
            } else {
                searchStatus.textContent = `❌ Erro: ${data.error}`;
                searchStatus.style.color = '#dc3545';
                searchStatus.style.fontWeight = '600';
            }
        } catch (error) {
            console.error('Erro ao finalizar visitas:', error);
            searchStatus.textContent = '❌ Erro de comunicação ao tentar finalizar as visitas.';
            searchStatus.style.color = '#dc3545';
            searchStatus.style.fontWeight = '600';
        }
    }

    function handleFaceAccepted() {
        if (!recognitionSession || processingRecognition) return;
        processingRecognition = true;
        recognitionSession.pause();
        sendFrameForRecognition();
    }

    function handleFaceTooFar() {
        if (!processingRecognition) {
            updateCameraStatus('Aproxime-se um pouco mais da câmera para finalizar visita.', false, '#ffc107');
        }
    }

    function handleFaceLost() {
        if (!processingRecognition) {
            updateCameraStatus('Posicione seu rosto na área da câmera para finalizar visita.', false, '#6c757d');
        }
    }

    try {
        recognitionSession = createMediaPipeRecognitionSession({
            videoElement: video,
            overlayElement: overlay,
            videoConstraints: {
                width: { ideal: 800, max: 1280 },
                height: { ideal: 800, max: 1280 },
                aspectRatio: { ideal: 1 }
            },
            desiredFaceWidthPercent: 0.25,
            statusUpdater: (message, spinner, color) => updateCameraStatus(message, spinner, color),
            onFaceAccepted: handleFaceAccepted,
            onFaceTooFar: handleFaceTooFar,
            onFaceLost: handleFaceLost,
            messages: {
                loading: '🤖 Carregando modelo de IA para finalizar visita...',
                camera: '📹 Iniciando câmera...',
                ready: '🎉 Sistema pronto! Posicione seu rosto para finalizar visita.',
                prompt: '👤 Posicione seu rosto na área da câmera para finalizar visita.'
            }
        });
        const resetDimensions = () => {
            video.width = 800;
            video.height = 800;
            overlay.width = 800;
            overlay.height = 800;
            overlay.style.width = '100%';
            overlay.style.height = '100%';
        };

        video.addEventListener('loadedmetadata', () => {
            resetDimensions();
            recognitionSession.start();
        }, { once: true });
    } catch (err) {
        console.error('Erro ao iniciar o reconhecimento facial:', err);
        updateCameraStatus('Erro ao inicializar o reconhecimento facial.', false, '#dc3545');
    }

    async function searchVisitor(query) {
        if (!query || query.length < 3) {
            searchStatus.textContent = '';
            return;
        }

        searchSpinner.style.display = 'block';
        searchStatus.textContent = '';

        try {
            const response = await fetch(`${searchVisitorUrl}?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (response.ok && data.success && data.visitantes.length > 0) {
                const visitor = data.visitantes[0];
                currentVisitorId = visitor.id;
                visitorNameSpan.textContent = visitor.nome;
                visitListUl.innerHTML = '';

                if (visitor.visitas.length > 0) {
                    visitor.visitas.forEach(visita => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';
                        li.textContent = `Visita ao ${visita.setor} - Entrada: ${visita.data_entrada}`;
                        visitListUl.appendChild(li);
                    });
                    visitListUl.style.display = 'block';
                    noVisitsMessageDiv.style.display = 'none';
                    confirmFinalizeBtn.style.display = 'block';
                } else {
                    visitListUl.style.display = 'none';
                    noVisitsMessageDiv.innerHTML = `<strong>${visitor.nome}</strong> foi encontrado, mas não possui visitas em andamento.`;
                    noVisitsMessageDiv.style.display = 'block';
                    confirmFinalizeBtn.style.display = 'none';
                }
                finalizeModal.show();
            } else {
                searchStatus.textContent = data.error || 'Nenhum visitante com visitas em andamento encontrado.';
            }
        } catch (error) {
            searchStatus.textContent = 'Erro de comunicação com o servidor.';
            console.error('Erro ao buscar visitante:', error);
        } finally {
            searchSpinner.style.display = 'none';
        }
    }

    async function finalizeVisits() {
        if (!currentVisitorId) return;

        try {
            const response = await fetch(finalizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ visitante_id: currentVisitorId })
            });
            const data = await response.json();

            finalizeModal.hide();
            if (data.success) {
                searchStatus.textContent = `✅ ${data.message}`;
                searchStatus.style.color = '#28a745';
                searchStatus.style.fontWeight = '600';
                searchInput.value = '';
                setTimeout(() => {
                    window.location.href = welcomeUrl;
                }, 3000);
            } else {
                searchStatus.textContent = `❌ Erro: ${data.error}`;
                searchStatus.style.color = '#dc3545';
                searchStatus.style.fontWeight = '600';
            }
        } catch (error) {
            console.error('Erro ao finalizar visitas:', error);
            searchStatus.textContent = '❌ Erro de comunicação ao tentar finalizar as visitas.';
            searchStatus.style.color = '#dc3545';
            searchStatus.style.fontWeight = '600';
        }
    }

    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchVisitor(searchInput.value);
        }, 500);
    });

    confirmFinalizeBtn.addEventListener('click', finalizeVisits);
});
