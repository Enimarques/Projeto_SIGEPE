const DEFAULT_ASSETS = {
    bundleCdn: 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js',
    wasmCdn: 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm',
    modelCdn: 'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite'
};

const DEFAULT_CONSTRAINTS = {
    width: { ideal: 800, max: 1280 },
    height: { ideal: 800, max: 1280 },
    aspectRatio: { ideal: 1.0 }
};

let cachedFaceDetectorPromise = null;

async function ensureFaceDetector(assetsOverride = {}) {
    if (cachedFaceDetectorPromise) {
        return cachedFaceDetectorPromise;
    }

    cachedFaceDetectorPromise = (async () => {
        const bundleUrl = assetsOverride.bundleCdn || DEFAULT_ASSETS.bundleCdn;
        const module = await import(bundleUrl);
        const { FaceDetector, FilesetResolver } = module;

        const wasmUrl = assetsOverride.wasmCdn || DEFAULT_ASSETS.wasmCdn;
        const modelUrl = assetsOverride.modelCdn || DEFAULT_ASSETS.modelCdn;

        const filesetResolver = await FilesetResolver.forVisionTasks(wasmUrl);
        const detector = await FaceDetector.createFromOptions(filesetResolver, {
            baseOptions: { modelAssetPath: modelUrl },
            runningMode: 'VIDEO'
        });
        return detector;
    })();

    return cachedFaceDetectorPromise;
}

function drawOverlay(ctx, boundingBox, color = '#28a745') {
    const { originX, originY, width, height } = boundingBox;
    const cornerLength = Math.min(width, height) * 0.25;

    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';

    // Top-left
    ctx.beginPath();
    ctx.moveTo(originX, originY + cornerLength);
    ctx.lineTo(originX, originY);
    ctx.lineTo(originX + cornerLength, originY);
    ctx.stroke();

    // Top-right
    ctx.beginPath();
    ctx.moveTo(originX + width - cornerLength, originY);
    ctx.lineTo(originX + width, originY);
    ctx.lineTo(originX + width, originY + cornerLength);
    ctx.stroke();

    // Bottom-left
    ctx.beginPath();
    ctx.moveTo(originX + cornerLength, originY + height);
    ctx.lineTo(originX, originY + height);
    ctx.lineTo(originX, originY + height - cornerLength);
    ctx.stroke();

    // Bottom-right
    ctx.beginPath();
    ctx.moveTo(originX + width - cornerLength, originY + height);
    ctx.lineTo(originX + width, originY + height);
    ctx.lineTo(originX + width, originY + height - cornerLength);
    ctx.stroke();
}

function clearOverlay(ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function updateStatus(statusUpdater, message, spinner = false, color = null) {
    if (typeof statusUpdater !== 'function') return;
    statusUpdater(message || '', spinner, color);
}

export function createMediaPipeRecognitionSession(config) {
    if (!config || !config.videoElement || !config.overlayElement) {
        throw new Error('videoElement e overlayElement são necessários.');
    }

    const videoElement = config.videoElement;
    const overlayElement = config.overlayElement;
    const ctx = overlayElement.getContext('2d');
    const desiredFaceWidthPercent = typeof config.desiredFaceWidthPercent === 'number' ? config.desiredFaceWidthPercent : 0.25;
    const videoConstraints = config.videoConstraints || DEFAULT_CONSTRAINTS;
    const assets = config.assets || {};
    const antiSpoofingConfig = config.antiSpoofing || { enabled: false };

    const statusUpdater = config.statusUpdater || (() => {});
    const onFaceAccepted = config.onFaceAccepted || (() => {});
    const onFaceTooFar = config.onFaceTooFar || (() => {});
    const onFaceLost = config.onFaceLost || (() => {});
    const onError = config.onError || (() => {});

    let faceDetector = null;
    let stream = null;
    let animationFrameId = null;
    let running = false;
    let paused = false;
    let hasAcceptedFace = false;

    function handleDetections(detections) {
        if (!detections || detections.length === 0) {
            hasAcceptedFace = false;
            clearOverlay(ctx);
            onFaceLost();
            updateStatus(statusUpdater, config.messages?.prompt || '👤 Posicione seu rosto na área da câmera.', false);
            return;
        }

        const face = detections[0].boundingBox;
        const faceWidthPercent = face.width / videoElement.videoWidth;
        drawOverlay(ctx, face, '#28a745');

        if (faceWidthPercent >= desiredFaceWidthPercent) {
            if (!hasAcceptedFace) {
                hasAcceptedFace = true;
                onFaceAccepted({ face, faceWidthPercent });
            }
            updateStatus(statusUpdater, config.messages?.analyzing || '🎯 Analisando rosto...', true, '#28a745');
        } else {
            hasAcceptedFace = false;
            onFaceTooFar();
            updateStatus(statusUpdater, config.messages?.closer || '📏 Aproxime-se um pouco mais da câmera.', false, '#ffc107');
        }
    }

    function loop() {
        if (!running) return;
        if (paused) {
            animationFrameId = requestAnimationFrame(loop);
            return;
        }

        try {
            const detections = faceDetector.detectForVideo(videoElement, Date.now()).detections;
            handleDetections(detections);
        } catch (err) {
            console.error('Erro no loop de detecção:', err);
            onError(err);
        }

        animationFrameId = requestAnimationFrame(loop);
    }

    async function start() {
        if (running) return;
        running = true;
        paused = false;
        updateStatus(statusUpdater, config.messages?.loading || '🤖 Carregando modelo de IA...', true);

        try {
            faceDetector = await ensureFaceDetector(assets);
            updateStatus(statusUpdater, config.messages?.camera || '📹 Iniciando câmera...', true);
            stream = await navigator.mediaDevices.getUserMedia({ video: videoConstraints });
            videoElement.srcObject = stream;

            await new Promise(resolve => {
                if (videoElement.readyState >= 2) {
                    resolve();
                } else {
                    videoElement.addEventListener('loadeddata', resolve, { once: true });
                }
            });

            overlayElement.width = videoElement.videoWidth;
            overlayElement.height = videoElement.videoHeight;
            overlayElement.style.width = '100%';
            overlayElement.style.height = '100%';

            updateStatus(statusUpdater, config.messages?.ready || '🎉 Sistema pronto! Posicione seu rosto.', false, '#28a745');
            loop();
        } catch (err) {
            console.error('Erro ao iniciar reconhecimento facial:', err);
            updateStatus(statusUpdater, config.messages?.error || '❌ Erro ao inicializar o reconhecimento facial.', false, '#dc3545');
            onError(err);
            stop();
        }
    }

    function pause() {
        paused = true;
    }

    function resume() {
        if (!running) return;
        paused = false;
        hasAcceptedFace = false; // Reset the accepted face flag when resuming
    }

    function stop() {
        running = false;
        paused = false;
        hasAcceptedFace = false;
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        clearOverlay(ctx);
    }

    return {
        start,
        stop,
        pause,
        resume,
        isRunning: () => running && !paused
    };
}