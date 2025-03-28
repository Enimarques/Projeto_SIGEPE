import cv2
import mediapipe as mp
import numpy as np
import os
import face_recognition
from datetime import datetime

class ReconhecimentoFacial:
    def __init__(self):
        # MediaPipe para desenho e detecção
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_desenho = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
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
            nome_arquivo_imagem = f"{self.diretorio_faces}/visitante_{id_visitante}_{timestamp}.jpg"
            nome_arquivo_encoding = f"{self.diretorio_faces}/visitante_{id_visitante}_{timestamp}.npy"
            
            cv2.imwrite(nome_arquivo_imagem, face_imagem)
            np.save(nome_arquivo_encoding, face_encoding)
            
            return nome_arquivo_encoding
            
        except Exception as e:
            print(f"Erro ao registrar face: {str(e)}")
            return None

    def verificar_face(self, frame):
        """Verifica se a face corresponde a algum visitante cadastrado"""
        try:
            # Converter para RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar faces no frame
            faces = face_recognition.face_locations(rgb_frame)
            if not faces:
                return None
                
            # Pegar a primeira face detectada
            face_location = faces[0]
            face_encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]
            
            # Procurar por matches nas faces cadastradas
            for arquivo in os.listdir(self.diretorio_faces):
                if arquivo.endswith('.npy'):
                    encoding_conhecido = np.load(os.path.join(self.diretorio_faces, arquivo))
                    
                    # Comparar faces
                    matches = face_recognition.compare_faces([encoding_conhecido], face_encoding, tolerance=0.6)
                    if matches[0]:
                        # Extrair ID do visitante do nome do arquivo
                        id_visitante = arquivo.split('_')[1]
                        return id_visitante
            
            return None
            
        except Exception as e:
            print(f"Erro ao verificar face: {str(e)}")
            return None

    def desenhar_face(self, frame):
        """Desenha os pontos faciais usando MediaPipe"""
        try:
            # Converter para RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar pontos faciais
            resultados = self.face_mesh.process(rgb_frame)
            
            if resultados.multi_face_landmarks:
                for face_landmarks in resultados.multi_face_landmarks:
                    # Desenhar a malha facial
                    self.mp_desenho.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_desenho.DrawingSpec(
                            color=(0, 255, 0), thickness=1, circle_radius=1
                        )
                    )
                return True
                
            return False
            
        except Exception as e:
            print(f"Erro ao desenhar face: {str(e)}")
            return False
