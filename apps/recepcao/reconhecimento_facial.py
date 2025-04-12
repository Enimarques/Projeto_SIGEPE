import cv2
import numpy as np
import os
import face_recognition
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Mock do face_recognition para permitir a execução sem ele
class MockFaceRecognition:
    @staticmethod
    def face_locations(image):
        return [(0, 100, 100, 0)]  # (top, right, bottom, left)
    
    @staticmethod
    def face_encodings(image, locations=None):
        return [np.zeros(128)]  # Encoding vazio
    
    @staticmethod
    def compare_faces(known_encodings, encoding, tolerance=0.6):
        return [False] * len(known_encodings)
    
    @staticmethod
    def face_distance(known_encodings, encoding):
        return [1.0] * len(known_encodings)
    
    @staticmethod
    def load_image_file(image_path):
        return cv2.imread(image_path)

# Substitua o módulo face_recognition pelo mock
face_recognition = MockFaceRecognition()

# Esta classe foi substituída pelo FaceRecognitionManager
# Mantida apenas para referência histórica e compatibilidade
class ReconhecimentoFacial:
    def __init__(self):
        # Diretório para armazenar as imagens faciais
        self.diretorio_faces = "media/faces"
        if not os.path.exists(self.diretorio_faces):
            os.makedirs(self.diretorio_faces)

    def registrar_face(self, imagem_path, id_visitante):
        """Registra a face do visitante a partir de uma imagem"""
        try:
            # Carregar a imagem
            imagem = cv2.imread(imagem_path)
            if imagem is None:
                return None
                
            # Converter para RGB (face_recognition requer RGB)
            rgb_imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            
            # Detectar faces na imagem
            faces = face_recognition.face_locations(rgb_imagem)
            if not faces:
                return None
                
            # Pegar a primeira face detectada
            face_location = faces[0]
            top, right, bottom, left = face_location
            
            # Extrair a região da face
            face_imagem = imagem[top:bottom, left:right]
            
            # Gerar encodings da face
            face_encoding = face_recognition.face_encodings(rgb_imagem, [face_location])[0]
            
            # Salvar a imagem da face e os encodings
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            face_filename = f"{id_visitante}_{timestamp}.jpg"
            face_path = os.path.join(self.diretorio_faces, face_filename)
            
            cv2.imwrite(face_path, face_imagem)
            
            # Retornar o caminho da imagem salva
            return face_path
            
        except Exception as e:
            print(f"Erro ao registrar face: {str(e)}")
            return None

    def detectar_face(self, frame):
        """Detecta faces em um frame de vídeo"""
        try:
            # Converter para RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar faces
            faces = face_recognition.face_locations(rgb_frame)
            
            if not faces:
                return None
                
            # Retornar a primeira face encontrada
            return faces[0]
            
        except Exception as e:
            print(f"Erro ao detectar face: {str(e)}")
            return None

    def comparar_faces(self, face_encoding1, face_encoding2, tolerancia=0.6):
        """Compara duas faces e retorna True se forem da mesma pessoa"""
        try:
            # Calcular a distância entre os encodings
            distancia = face_recognition.face_distance([face_encoding1], face_encoding2)[0]
            return distancia <= tolerancia
            
        except Exception as e:
            print(f"Erro ao comparar faces: {str(e)}")
            return False

    def validate_image(self, image):
        # Verificar tamanho máximo
        if image.size > 5 * 1024 * 1024:  # 5MB
            raise ValueError("Imagem muito grande")
            
        # Verificar formato
        if not image.content_type in ['image/jpeg', 'image/png']:
            raise ValueError("Formato de imagem não suportado")

    def register_face(self, visitante_id, max_attempts=3):
        # Simulando registro bem-sucedido
        return True

    def draw_face_boxes(self, frame, face_locations, face_ids):
        for (top, right, bottom, left), face_id in zip(face_locations, face_ids):
            # Código existente...
            
            # Adicionar indicador de confiança
            if face_id:
                confidence = self.calculate_confidence(face_id)
                cv2.putText(frame, f"Confiança: {confidence:.2f}%", 
                           (left, bottom + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

class FaceRecognitionManager:
    def load_known_faces(self):
        cached_encodings = cache.get('face_encodings')
        if cached_encodings:
            self.known_face_encodings, self.known_face_ids = cached_encodings
            return
        
        # Carregar do banco se não estiver em cache
        visitantes = Visitante.objects.filter(face_registrada=True)
        # ... resto do código ...
        
        # Armazenar em cache
        cache.set('face_encodings', (self.known_face_encodings, self.known_face_ids), 3600)

class EnhancedFaceRecognitionManager(FaceRecognitionManager):
    def __init__(self):
        super().__init__()
        self.spoof_detector = self._load_spoof_detector()
        self.emotion_detector = self._load_emotion_detector()
        
    def _load_spoof_detector(self):
        # Implementar detector de spoofing
        pass
        
    def _load_emotion_detector(self):
        # Implementar detector de emoções
        pass
        
    def process_frame(self, frame):
        """Processamento avançado de frame"""
        try:
            # Detecção de spoofing
            is_spoof = self.spoof_detector.detect(frame)
            if is_spoof:
                logger.warning("Tentativa de spoofing detectada")
                return None
                
            # Detecção de emoções
            emotions = self.emotion_detector.detect(frame)
            
            # Reconhecimento facial original
            face_locations, face_ids = self.identify_face(frame)
            
            return {
                'faces': list(zip(face_locations, face_ids)),
                'emotions': emotions,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de frame: {str(e)}")
            return None
