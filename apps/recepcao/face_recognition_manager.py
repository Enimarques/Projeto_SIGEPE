import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from django.conf import settings
from django.db import connection
from .models import Visitante
import concurrent.futures

class FaceRecognitionManager:
    def __init__(self, tolerance=0.6):
        self.known_face_encodings = []
        self.known_face_ids = []
        self.tolerance = tolerance  # Tolerância para reconhecimento (menor = mais preciso)
        self.enabled = settings.FACE_RECOGNITION_SETTINGS.get('ENABLED', True)
        # Não é mais necessário carregar modelos manualmente
        # O pacote face_recognition_models já fornece os modelos necessários
        # via face_recognition
        # self.shape_predictor = dlib.shape_predictor(LANDMARKS_MODEL)
        # self.face_rec_model = dlib.face_recognition_model_v1(RECOGNITION_MODEL)
        # self.cnn_face_detector = dlib.cnn_face_detection_model_v1(CNN_DETECTOR_MODEL)
        
        # Verifica se a tabela existe antes de carregar as faces
        if self.table_exists('recepcao_visitante'):
            self.load_known_faces()
            print(f"FaceRecognitionManager inicializado com {len(self.known_face_encodings)} faces conhecidas")
            print(f"Reconhecimento facial está {'HABILITADO' if self.enabled else 'DESABILITADO'}")
        else:
            print("Tabela de visitantes não existe. Pulando carregamento de faces.")

    def table_exists(self, table_name):
        """Verifica se uma tabela existe no banco de dados"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM sqlite_master
                    WHERE type='table' AND name=%s;
                    """,
                    [table_name]
                )
                return cursor.fetchone()[0] > 0
        except:
            return False

    def load_known_faces(self):
        """Carrega todos os rostos registrados do banco de dados"""
        if not self.enabled:
            print("Reconhecimento facial desabilitado. Não carregando faces...")
            return
            
        visitantes = Visitante.objects.filter(face_registrada=True)
        print(f"Carregando faces de {visitantes.count()} visitantes registrados")
        
        for visitante in visitantes:
            if visitante.foto:
                try:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(visitante.foto))
                    if os.path.exists(image_path):
                        print(f"Processando foto do visitante {visitante.nome_completo} (ID: {visitante.id})")
                        image = cv2.imread(image_path)
                        if image is None:
                            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
                        
                        print(f"Dimensões da imagem: {image.shape}")
                        print(f"Tipo de dados da imagem: {image.dtype}")
                        
                        # Pré-processamento da imagem
                        # 1. Converter para tons de cinza
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        
                        # 2. Aplicar equalização de histograma para melhorar o contraste
                        gray = cv2.equalizeHist(gray)
                        
                        # 3. Converter de volta para RGB (3 canais)
                        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
                        
                        # 4. Garantir que a imagem esteja no formato uint8
                        if image.dtype != np.uint8:
                            image = image.astype(np.uint8)
                        
                        print(f"Tipo de dados após processamento: {image.dtype}")
                        print(f"Valores mínimos e máximos: {image.min()}, {image.max()}")
                        
                        # Detectar localizações de rostos primeiro
                        face_locations = face_recognition.face_locations(image)
                        if not face_locations:
                            print(f"ERRO: Nenhum rosto detectado na foto do visitante {visitante.nome_completo}")
                            raise ValueError("Nenhum rosto detectado na foto. Tente novamente com uma foto mais clara do rosto.")
                        
                        print(f"Rostos detectados: {len(face_locations)}")
                        
                        # Gerar encodings apenas com as localizações já detectadas
                        face_encodings = face_recognition.face_encodings(image, face_locations)

                        if not face_encodings:
                            print(f"ERRO: Não foi possível gerar encodings para o rosto detectado")
                            raise ValueError("Não foi possível processar o rosto na imagem. A imagem pode estar muito escura ou desfocada.")

                        # Atualiza o visitante
                        visitante.face_registrada = True
                        visitante.face_id = str(datetime.now().timestamp())  # ID único baseado no timestamp
                        visitante.save()
                        print(f"Visitante atualizado: face_registrada={visitante.face_registrada}, face_id={visitante.face_id}")

                        # Atualiza os arrays locais
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_ids.append(visitante.id)
                        print(f"Face do visitante {visitante.nome_completo} registrada com sucesso. Total de faces conhecidas: {len(self.known_face_encodings)}")
                except Exception as e:
                    print(f"ERRO ao carregar face do visitante {visitante.id}: {str(e)}")

    def register_face(self, visitante_id):
        """Registra um novo rosto para um visitante"""
        if not self.enabled:
            print("Reconhecimento facial desabilitado. Simulando registro com sucesso...")
            visitante = Visitante.objects.get(id=visitante_id)
            visitante.face_registrada = True
            visitante.face_id = str(datetime.now().timestamp())
            visitante.save()
            return True
            
        try:
            visitante = Visitante.objects.get(id=visitante_id)
            print(f"Iniciando registro de face para visitante: {visitante.nome_completo} (ID: {visitante_id})")
            
            if not visitante.foto:
                raise ValueError("Visitante não possui foto cadastrada")

            image_path = os.path.join(settings.MEDIA_ROOT, str(visitante.foto))
            if not os.path.exists(image_path):
                raise ValueError(f"Arquivo de foto não encontrado: {image_path}")

            # Carrega a imagem e detecta o rosto
            print(f"Carregando imagem: {image_path}")
            image = face_recognition.load_image_file(image_path)
            print(f"Dimensões da imagem: {image.shape}")
            
            # Detectar localizações de rostos primeiro
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                print(f"ERRO: Nenhum rosto detectado na foto do visitante {visitante.nome_completo}")
                raise ValueError("Nenhum rosto detectado na foto. Tente novamente com uma foto mais clara do rosto.")
                
            print(f"Rostos detectados: {len(face_locations)}")
            
            # Gerar encodings apenas com as localizações já detectadas
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if not face_encodings:
                print(f"ERRO: Não foi possível gerar encodings para o rosto detectado")
                raise ValueError("Não foi possível processar o rosto na imagem. A imagem pode estar muito escura ou desfocada.")

            # Atualiza o visitante
            visitante.face_registrada = True
            visitante.face_id = str(datetime.now().timestamp())  # ID único baseado no timestamp
            visitante.save()
            print(f"Visitante atualizado: face_registrada={visitante.face_registrada}, face_id={visitante.face_id}")

            # Atualiza os arrays locais
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_ids.append(visitante.id)
            print(f"Face do visitante {visitante.nome_completo} registrada com sucesso. Total de faces conhecidas: {len(self.known_face_encodings)}")

            return True
        except Exception as e:
            import traceback
            print(f"ERRO ao registrar face: {str(e)}")
            print(traceback.format_exc())
            raise

    def identify_face(self, frame, tolerance=None, max_attempts=5):
        """Identifica rostos em um frame de vídeo. Usa apenas modelo HOG. Limita tentativas."""
        if not self.enabled:
            print("Reconhecimento facial desabilitado. Retornando sem identificação...")
            return [], []
        if tolerance is None:
            tolerance = self.tolerance
        try:
            import time
            start_time = time.time()
            if frame is None:
                print("ERRO: Frame vazio recebido para identificação")
                return [], []
            print(f"Processando frame para identificação. Dimensões: {frame.shape}")
            if len(self.known_face_encodings) == 0:
                print("AVISO: Nenhuma face conhecida cadastrada no sistema")
                return [], []
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            print("Detectando faces no frame (modelo HOG)...")
            attempts = 0
            face_locations = []
            while attempts < max_attempts and not face_locations:
                face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
                attempts += 1
            if not face_locations:
                print(f"Nenhum rosto detectado no frame após {attempts} tentativas")
                return [], []
            print(f"Rostos detectados: {len(face_locations)}")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            print(f"Encodings gerados: {len(face_encodings)}")
            face_ids = []
            def compare_encoding(face_encoding):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=tolerance)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding) if self.known_face_encodings else []
                min_distance = min(distances) if len(distances) > 0 else 1.0
                min_index = np.argmin(distances) if len(distances) > 0 else -1
                if True in matches:
                    first_match_index = matches.index(True)
                    face_id = self.known_face_ids[first_match_index]
                    print(f"Rosto reconhecido: ID={face_id}, distância={distances[first_match_index]:.4f}")
                    return face_id
                else:
                    print(f"Rosto não reconhecido. Melhor correspondência: {min_distance:.4f} (acima da tolerância {tolerance})")
                    return None
            # Multiprocessing para acelerar se houver muitos encodings
            if len(self.known_face_encodings) > 20:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    results = list(executor.map(compare_encoding, face_encodings))
                face_ids = results
            else:
                for face_encoding in face_encodings:
                    face_ids.append(compare_encoding(face_encoding))
            print(f"Tempo de processamento identify_face: {round(time.time() - start_time, 3)}s")
            return [(loc[0]*4, loc[1]*4, loc[2]*4, loc[3]*4) for loc in face_locations], face_ids
        except Exception as e:
            import traceback
            print(f"ERRO na identificação facial: {str(e)}")
            print(traceback.format_exc())
            return [], []

    def draw_face_boxes(self, frame, face_locations, face_ids):
        """Desenha caixas e informações ao redor dos rostos detectados"""
        try:
            for (top, right, bottom, left), face_id in zip(face_locations, face_ids):
                # Desenha a caixa ao redor do rosto
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Adiciona o nome do visitante se reconhecido
                if face_id is not None:
                    try:
                        visitante = Visitante.objects.get(id=face_id)
                        nome = visitante.nome_completo
                        cor = (0, 255, 0)  # Verde para reconhecido
                    except Visitante.DoesNotExist:
                        nome = "Desconhecido"
                        cor = (0, 0, 255)  # Vermelho para não reconhecido
                else:
                    nome = "Não Identificado"
                    cor = (0, 0, 255)  # Vermelho para não reconhecido

                # Desenha o fundo do texto
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
                
                # Adiciona o texto
                cv2.putText(frame, nome, (left + 6, bottom - 6), 
                          cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            return frame
        except Exception as e:
            print(f"ERRO ao desenhar caixas faciais: {str(e)}")
            return frame

    def reload_encodings(self):
        """Força o recarregamento dos encodings do banco de dados."""
        self.known_face_encodings = []
        self.known_face_ids = []
        self.load_known_faces()
        print(f"Encodings recarregados manualmente. Total: {len(self.known_face_encodings)}")
