class Camera {
    constructor(videoEl, canvasEl, photoPreviewEl, cameraPlaceholderEl, photoInputId, cameraContainerEl, cameraInfoEl, clearPhotoBtnEl) {
        this.video = videoEl;
        this.canvas = canvasEl;
        this.photoPreview = photoPreviewEl;
        this.cameraPlaceholder = cameraPlaceholderEl;
        this.photoInputId = photoInputId; // Armazenar o ID, não o elemento
        this.cameraContainer = cameraContainerEl;
        this.cameraInfo = cameraInfoEl;
        this.clearPhotoBtn = clearPhotoBtnEl;
        this.stream = null;
    }

    async startCamera() {
        try {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                this.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
                this.video.srcObject = this.stream;
                this.cameraContainer.style.display = 'block';
                this.cameraInfo.textContent = 'Posicione o rosto no centro do círculo.';
            } else {
                alert('Seu navegador não suporta acesso à câmera.');
            }
        } catch (err) {
            console.error("Erro ao iniciar a câmera: ", err);
            alert('Não foi possível acessar a câmera. Verifique as permissões do navegador.');
        }
    }

    capturePhoto() {
        const photoInput = document.getElementById(this.photoInputId); // Buscar o elemento no momento do uso
        if (!photoInput) {
            alert('ERRO FATAL: Campo de input da foto (id_foto) não foi encontrado no HTML. A captura não pode continuar.');
            return; // Interrompe a execução da função aqui.
        }

        const btnCapturar = document.getElementById('btnCapturarFoto');
        btnCapturar.disabled = true;
        btnCapturar.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';

        try {
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            this.canvas.getContext('2d').drawImage(this.video, 0, 0);

            this.canvas.toBlob((blob) => {
                const file = new File([blob], 'foto_webcam.jpg', { type: 'image/jpeg' });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                photoInput.files = dataTransfer.files; // Usar a variável local
                console.log('Arquivo de foto atribuído ao formulário.', photoInput.files);
                
                const imageUrl = URL.createObjectURL(blob);
                this.photoPreview.src = imageUrl;
                this.photoPreview.style.display = 'block';
                this.cameraPlaceholder.style.display = 'none';
                this.clearPhotoBtn.style.display = 'inline-block';
                
                this.stopCamera();

                btnCapturar.disabled = false;
                btnCapturar.innerHTML = '<i class="fas fa-camera-retro me-2"></i>Capturar Foto';
                
                alert('Foto capturada! Preencha o resto do formulário e clique em salvar.');

            }, 'image/jpeg', 0.9);
            
        } catch (err) {
            alert('Ocorreu um erro ao capturar a foto: ' + err.message);
            btnCapturar.disabled = false;
            btnCapturar.innerHTML = '<i class="fas fa-camera-retro me-2"></i>Capturar Foto';
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.cameraContainer.style.display = 'none';
        }
    }

    clearPhoto() {
        this.photoPreview.src = '';
        this.photoPreview.style.display = 'none';
        this.cameraPlaceholder.style.display = 'flex';
        this.clearPhotoBtn.style.display = 'none';
        
        const photoInput = document.getElementById(this.photoInputId); // Buscar o elemento no momento do uso
        if (photoInput) {
            photoInput.value = ''; // Limpa o valor do input file
        }
        this.stopCamera();
    }
}

// Inicializar quando o documento estiver pronto
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('btnIniciarCamera')) {
        const camera = new Camera(
            document.getElementById('video'),
            document.getElementById('canvas'),
            document.getElementById('photoPreview'),
            document.getElementById('cameraPlaceholder'),
            'fotoInput',
            document.getElementById('cameraContainer'),
            document.getElementById('cameraInfo'),
            document.getElementById('clearPhotoBtn')
        );
        camera.startCamera();
    }
}); 