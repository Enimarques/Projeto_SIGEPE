const DEFAULT_ASSETS = {
    bundleCdn: 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js',
    wasmCdn: 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm',
    modelCdn: 'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite'
};

const DEFAULT_CONSTRAINTS = {
    width: { ideal: 800, max: 1280 },
    height: { ideal: 800, max: 1280 },
    aspectRatio: { ideal: 1 }
};

const DEFAULT_MESSAGES = {
    loading: 'Carregando modelo de IA...',
    camera: 'Iniciando câmera...',
    prompt: 'Posicione seu rosto na área da câmera para iniciar reconhecimento.',
    closer: 'Aproxime-se um pouco mais da câmera.',
    analyzing: 'Ótimo! Analisando rosto...',
    noFace: '👤 Posicione seu rosto na área da câmera para iniciar identificação.',
    error: 'Erro ao acessar a câmera. Verifique permissões.'
};

let globalFaceDetectorPromise = null;

async function resolveUrl(localUrl, fallbackUrl) {
    if (!localUrl) {
        return fallbackUrl;
    }
    try {
        const response = await fetch(localUrl, { method: 'HEAD' });
        if (response.ok) {
            return localUrl;
        }
    } catch (err) {
        console.warn('Falha ao verificar recurso local:', localUrl, err);
    }
    return fallbackUrl;
}

async function ensureFaceDetector(assets) {
    if (globalFaceDetectorPromise) {
        return globalFaceDetectorPromise;
    }

    globalFaceDetectorPromise = (async () => {
        const bundleUrl = await resolveUrl(assets.bundleLocal, assets.bundleCdn);
        const module = await import(bundleUrl);
        const { FaceDetector, FilesetResolver } = module;

        const wasmUrl = await resolveUrl(assets.wasmLocal, assets.wasmCdn);
        const modelUrl = await resolveUrl(assets.modelLocal, assets.modelCdn);

        const filesetResolver = await FilesetResolver.forVisionTasks(wasmUrl);
        const detector = await FaceDetector.createFromOptions(filesetResolver, {
            baseOptions: { modelAssetPath: modelUrl },
            runningMode: 'VIDEO'
        });

        return detector;
    })();

    return globalFaceDetectorPromise;
}

function drawOverlay(ctx, box, color = '#ffc107') {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    if (!box) {
        return;
    }

    const { originX, originY, width, height } = box;
    const cornerLength = Math.min(width, height) * 0.25;
    const lineWidth = 6;
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    // Top-left
    ctx.beginPath();
    ctx.moveTo(originX + cornerLength, originY);
    ctx.lineTo(originX, originY);
    ctx.lineTo(originX, originY + cornerLength);
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

export function createFaceRecognitionSession(config) {
    if (!config || !config.videoElement || !config.overlayElement) {
        throw new Error('videoElement e overlayElement são obrigatórios.');
    }

    const assets = {
        ...DEFAULT_ASSETS,
        ...(config.assets || {})
    };

    const statusMessages = {
        ...DEFAULT_MESSAGES,
        ...(config.statusMessages || {})
    };

    const videoConstraints = config.videoConstraints || DEFAULT_CONSTRAINTS;
    const desiredFaceWidthPercent = typeof config.desiredFaceWidthPercent === 'number'
        ? config.desiredFaceWidthPercent
        : 0.25;

    const statusUpdater = typeof config.statusUpdater === 'function' ? config.statusUpdater : () => {};
    const onFaceReady = typeof config.onFaceReady === 'function' ? config.onFaceReady : () => {};
    const onFaceLost = typeof config.onFaceLost === 'function' ? config.onFaceLost : () => {};
    const onError = typeof config.onError === 'function' ? config.onError : () => {};

    let faceDetector = null;
    let ctx = config.overlayElement.getContext('2d');
    let stream = null;
    let animationFrameId = null;
    let running = false;
    let paused = false;
    let readyTriggered = false;

    async function start() {
        try {
            updateStatus(statusMessages.loading, true);
            faceDetector = await ensureFaceDetector(assets);
            updateStatus(statusMessages.camera, true);

            stream = await navigator.mediaDevices.getUserMedia({ video: videoConstraints });
            config.videoElement.srcObject = stream;

            await new Promise(resolve => {
                if (config.videoElement.readyState >= 2) {
                    resolve();
                    return;
                }
                config.videoElement.addEventListener('loadeddata', resolve, { once: true });
            });

            ctx.canvas.width = config.videoElement.videoWidth;
            ctx.canvas.height = config.videoElement.videoHeight;
            ctx.canvas.style.width = '100%';
            ctx.canvas.style.height = '100%';

            running = true;
            paused = false;
            readyTriggered = false;
            clearOverlay(ctx);
            updateStatus(statusMessages.prompt, false);
            loop();
        } catch (err) {
            console.error('Erro ao inicializar reconhecimento facial:', err);
            updateStatus(statusMessages.error, false);
            onError(err);
            stop();
            throw err;
        }
    }

    function stop() {
        running = false;
        paused = false;
        readyTriggered = false;
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

    function pause() {
        paused = true;
    }

    function resume() {
        if (!running) return;
        paused = false;
        readyTriggered = false;
    }

    function updateStatus(message, spinner = false) {
        statusUpdater(message || '', spinner);
    }

    function handleDetections(detections) {
        if (!detections || detections.length === 0) {
            readyTriggered = false;
            clearOverlay(ctx);
            onFaceLost();
            updateStatus(statusMessages.prompt, false);
            return;
        }

        const face = detections[0].boundingBox;
        const faceWidthPercent = face.width / config.videoElement.videoWidth;

        if (faceWidthPercent >= desiredFaceWidthPercent) {
            drawOverlay(ctx, face, '#28a745');
            updateStatus(statusMessages.analyzing, true);
            if (!readyTriggered) {
                readyTriggered = true;
                onFaceReady({ faceWidthPercent, face });
            }
        } else {
            readyTriggered = false;
            drawOverlay(ctx, face, '#ffc107');
            updateStatus(statusMessages.closer, false);
        }
    }

    function loop() {
        if (!running) {
            return;
        }
        if (paused) {
            animationFrameId = requestAnimationFrame(loop);
            return;
        }

        try {
            const detections = faceDetector.detectForVideo(config.videoElement, Date.now()).detections;
            handleDetections(detections);
        } catch (err) {
            console.error('Erro no loop de detecção:', err);
            onError(err);
        }

        animationFrameId = requestAnimationFrame(loop);
    }

    return {
        start,
        stop,
        pause,
        resume,
        isReady: () => readyTriggered
    };
}
