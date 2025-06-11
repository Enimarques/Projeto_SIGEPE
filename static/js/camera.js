class CameraManager {
    constructor() {
        this.stream = null;
        this.video = null;
        this.canvas = null;
        this.photoPreview = null;
        this.currentCameraLabel = '';
        this.photoInput = null;
        this.cameraPlaceholder = null;
        this.clearPhotoBtn = null;
        this.capturedPhoto = null;
    }

    async init() {
        // Inicializar elementos
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.photoPreview = document.getElementById('photoPreview');
        this.cameraPlaceholder = document.getElementById('cameraPlaceholder');
        this.clearPhotoBtn = document.getElementById('clearPhotoBtn');
        this.photoInput = document.getElementById('fotoInput');
        if (!this.photoInput) {
            this.photoInput = document.createElement('input');
            this.photoInput.type = 'hidden';
            this.photoInput.name = 'foto';
            this.photoInput.id = 'fotoInput';
            document.querySelector('form').appendChild(this.photoInput);
        }

        // Adicionar listeners
        document.getElementById('btnIniciarCamera')?.addEventListener('click', () => this.startCamera());
        document.getElementById('btnCapturarFoto')?.addEventListener('click', () => this.capturePhoto());
        document.getElementById('clearPhotoBtn')?.addEventListener('click', () => this.clearPhoto());
    }

    async getPhysicalCamera() {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(d => d.kind === 'videoinput');
        const physicalCamera = videoDevices.find(d => !/virtual|obs|manycam|droid/i.test(d.label));
        
        if (physicalCamera) {
            this.currentCameraLabel = physicalCamera.label;
            return { deviceId: { exact: physicalCamera.deviceId } };
        } else if (videoDevices.length > 0) {
            this.currentCameraLabel = videoDevices[0].label;
            return { deviceId: { exact: videoDevices[0].deviceId } };
        }
        throw new Error('Nenhuma câmera física encontrada.');
    }

    async startCamera() {
        const btnIniciarCamera = document.getElementById('btnIniciarCamera');
        const cameraContainer = document.getElementById('cameraContainer');
        const cameraInfo = document.getElementById('cameraInfo');
        const btnCapturarFoto = document.getElementById('btnCapturarFoto');

        btnIniciarCamera.disabled = true;
        try {
            const videoConstraints = await this.getPhysicalCamera();
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    ...videoConstraints, 
                    width: 640, 
                    height: 480 
                } 
            });
            this.video.srcObject = this.stream;
            await this.video.play();
            cameraContainer.style.display = 'block';
            cameraInfo.innerHTML = `<i class="fas fa-video me-2"></i>Usando: ${this.currentCameraLabel}`;
            btnCapturarFoto.disabled = false;
        } catch (err) {
            alert('Erro ao acessar a câmera: ' + err.message);
            btnIniciarCamera.disabled = false;
        }
    }

    capturePhoto() {
        if (!this.video || this.video.readyState < 3) {
            alert('A câmera não está pronta. Tente novamente.');
            return;
        }

        const btnCapturar = document.getElementById('btnCapturarFoto');
        btnCapturar.disabled = true;
        btnCapturar.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';

        try {
            // Configurar canvas
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            
            // Capturar frame
            const ctx = this.canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);
            
            // Converter para base64
            this.capturedPhoto = this.canvas.toDataURL('image/jpeg', 0.8);
            
            // Atualizar preview
            this.photoPreview.src = this.capturedPhoto;
            this.photoPreview.style.display = 'block';
            this.cameraPlaceholder.style.display = 'none';
            this.clearPhotoBtn.style.display = 'inline-block';
            
            // Atualizar input hidden
            this.photoInput.value = this.capturedPhoto;
            
            // Parar câmera e resetar UI
            this.stopCamera();
        } catch (err) {
            alert('Erro ao capturar foto: ' + err.message);
        } finally {
            btnCapturar.disabled = false;
            btnCapturar.innerHTML = '<i class="fas fa-camera me-2"></i>Capturar Foto';
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        document.getElementById('cameraContainer').style.display = 'none';
        document.getElementById('btnIniciarCamera').disabled = false;
        document.getElementById('btnCapturarFoto').disabled = true;
    }

    clearPhoto() {
        this.photoPreview.style.display = 'none';
        this.cameraPlaceholder.style.display = 'flex';
        this.clearPhotoBtn.style.display = 'none';
        this.photoInput.value = '';
        this.capturedPhoto = null;
    }
}

// Inicializar quando o documento estiver pronto
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('btnIniciarCamera')) {
        const camera = new CameraManager();
        camera.init();
    }
}); 