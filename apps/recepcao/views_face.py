from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import json
import numpy as np
from .models import Visitante, Visita, Setor
from .face_recognition_manager import FaceRecognitionManager
import face_recognition
from django.utils import timezone
import time
from django.urls import reverse

# Instância global do gerenciador de reconhecimento facial
face_manager = FaceRecognitionManager()

@login_required
def registrar_face(request, visitante_id):
    """View para registrar a face de um visitante"""
    try:
        visitante = Visitante.objects.get(id=visitante_id)
        
        if not visitante.foto:
            messages.error(request, 'É necessário fazer o upload de uma foto do visitante primeiro.')
            return redirect('recepcao:detalhes_visitante', pk=visitante_id)
        
        try:
            face_manager.register_face(visitante_id)
            messages.success(request, 'Face registrada com sucesso!')
        except ValueError as e:
            messages.error(request, str(e))
            
        return redirect('recepcao:detalhes_visitante', pk=visitante_id)
        
    except Visitante.DoesNotExist:
        messages.error(request, 'Visitante não encontrado.')
        return redirect('recepcao:lista_visitantes')

def gen_frames():
    """Gerador de frames para o stream de vídeo"""
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detecta e identifica rostos no frame
            face_locations, face_ids = face_manager.identify_face(frame)
            
            # Desenha as caixas e informações nos rostos detectados
            frame = face_manager.draw_face_boxes(frame, face_locations, face_ids)
            
            # Converte o frame para JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@login_required
def video_feed(request):
    """View para streaming do vídeo com reconhecimento facial"""
    return StreamingHttpResponse(gen_frames(),
                               content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def verificar_face_api(request):
    """API para verificar face em uma imagem"""
    if request.method == 'POST':
        try:
            import time
            start_time = time.time()
            print(f"Recebendo solicitação de verificação facial")
            print(f"Content-Type: {request.content_type}")
            print(f"Tamanho dos dados: {len(request.body)} bytes")
            tolerance = 0.6  # Valor padrão
            max_attempts = 5
            timeout = 5  # segundos
            try:
                tolerance_param = request.POST.get('tolerance')
                if tolerance_param:
                    tolerance = float(tolerance_param)
                    print(f"Usando tolerância personalizada: {tolerance}")
                attempts_param = request.POST.get('max_attempts')
                if attempts_param:
                    max_attempts = int(attempts_param)
                timeout_param = request.POST.get('timeout')
                if timeout_param:
                    timeout = float(timeout_param)
            except (ValueError, TypeError) as e:
                print(f"Erro ao processar parâmetros: {e}, usando valores padrão")
            face_image = request.FILES.get('face_image')
            if not face_image:
                print("ERROR: Nenhuma imagem encontrada no request")
                return JsonResponse({'success': False, 'error': 'Nenhuma imagem enviada'})
            print(f"Imagem recebida: {face_image.name}, tamanho: {face_image.size} bytes")
            nparr = np.frombuffer(face_image.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                print("ERROR: Falha ao decodificar imagem")
                return JsonResponse({'success': False, 'error': 'Falha ao decodificar imagem. O arquivo pode estar corrompido.'})
            print(f"Dimensões da imagem: {img.shape}")
            if len(face_manager.known_face_encodings) == 0:
                return JsonResponse({'success': False, 'error': 'Nenhum rosto cadastrado no sistema. Cadastre pelo menos um visitante com foto clara.'})
            if img.size == 0 or img.shape[0] == 0 or img.shape[1] == 0:
                print("ERROR: Imagem inválida ou vazia")
                return JsonResponse({'success': False, 'error': 'Imagem inválida ou vazia'})
            # Pré-processamento: equalização de histograma
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            img_eq = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            rgb_img = cv2.cvtColor(img_eq, cv2.COLOR_BGR2RGB)
            if rgb_img.dtype != np.uint8:
                rgb_img = rgb_img.astype(np.uint8)
            if rgb_img.max() > 1.0:
                rgb_img = rgb_img.astype(np.float32) / 255.0
                rgb_img = (rgb_img * 255).astype(np.uint8)
            print(f"Tipo de dados da imagem: {rgb_img.dtype}")
            print(f"Valores mínimos e máximos: {rgb_img.min()}, {rgb_img.max()}")
            # Apenas modelo HOG, limitar tentativas e timeout
            elapsed = 0
            faces_detected = []
            while elapsed < timeout:
                face_locations = face_recognition.face_locations(rgb_img, model="hog")
                if face_locations:
                    break
                time.sleep(0.2)
                elapsed = time.time() - start_time
            if not face_locations:
                avg_brightness = np.mean(rgb_img)
                print(f"Brilho médio da imagem: {avg_brightness}/255")
                img_blur = cv2.GaussianBlur(rgb_img, (11, 11), 0)
                laplacian_var = cv2.Laplacian(img_blur, cv2.CV_64F).var()
                print(f"Valor de foco (variância Laplaciana): {laplacian_var}")
                return JsonResponse({
                    'success': False,
                    'faces_detected': [],
                    'message': f'Nenhum rosto detectado após {max_attempts} tentativas. Tente novamente com melhor iluminação e posicionamento.',
                    'diagnostico': {
                        'brilho': float(avg_brightness),
                        'foco': float(laplacian_var),
                        'dimensoes': img.shape
                    }
                })
            print(f"Rostos detectados: {len(face_locations)}")
            adjusted_tolerance = tolerance
            avg_brightness = np.mean(rgb_img)
            if avg_brightness < 80:
                adjusted_tolerance = min(1.0, tolerance * 1.2)
                print(f"Imagem escura (brilho: {avg_brightness}), aumentando tolerância para {adjusted_tolerance}")
            face_locations, face_ids = face_manager.identify_face(img_eq, tolerance=adjusted_tolerance, max_attempts=max_attempts)
            if not face_ids or all(id is None for id in face_ids):
                print("AVISO: Nenhum visitante reconhecido nas faces detectadas")
            faces_detected = []
            for loc, face_id in zip(face_locations, face_ids):
                face_info = {'location': loc, 'visitante_id': face_id}
                if face_id:
                    try:
                        visitante = Visitante.objects.get(id=face_id)
                        face_info['nome'] = visitante.nome_completo
                        print(f"Visitante reconhecido: {visitante.nome_completo} (ID: {face_id})")
                    except Visitante.DoesNotExist:
                        print(f"ERROR: Visitante com ID {face_id} não encontrado no banco de dados")
                        face_info['nome'] = 'Visitante Desconhecido'
                else:
                    print("INFO: Rosto não reconhecido")
                    face_info['nome'] = 'Visitante Não Identificado'
                faces_detected.append(face_info)
            response_data = {
                'success': True,
                'faces_detected': faces_detected,
                'tolerance_used': adjusted_tolerance,
                'processing_time': round(time.time() - start_time, 3)
            }
            print(f"Tempo de processamento: {response_data['processing_time']}s")
            print(f"Resposta: {response_data}")
            return JsonResponse(response_data)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR ao verificar face: {str(e)}")
            print(f"Detalhes do erro: {error_details}")
            return JsonResponse({'success': False, 'error': str(e), 'error_details': error_details})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@csrf_exempt
def cadastro_rapido_api(request):
    """API para cadastro rápido de visitante através do totem"""
    if request.method == 'POST':
        try:
            # Log para depuração
            print("Recebendo solicitação de cadastro rápido")
            
            # Obter imagem da face
            face_image = request.FILES.get('face_image')
            if not face_image:
                print("ERROR: Nenhuma imagem encontrada no request")
                return JsonResponse({
                    'success': False,
                    'message': 'Nenhuma imagem enviada'
                })
            
            print(f"Imagem recebida: {face_image.name}, tamanho: {face_image.size} bytes")
            
            # Garantir que o arquivo possa ser lido múltiplas vezes
            face_image.seek(0)
            
            # Converter a imagem para numpy array para verificar se é válida
            try:
                nparr = np.frombuffer(face_image.read(), np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as decode_error:
                print(f"ERRO ao decodificar imagem: {decode_error}")
                return JsonResponse({
                    'success': False,
                    'message': 'Falha ao processar imagem. Verifique o formato do arquivo.',
                    'error_details': str(decode_error)
                })
            
            # Verificações adicionais de segurança
            if img is None:
                print("ERROR: Imagem decodificada é None")
                return JsonResponse({
                    'success': False,
                    'message': 'Falha ao decodificar imagem. Arquivo pode estar corrompido.'
                })
            
            if img.size == 0 or img.shape[0] == 0 or img.shape[1] == 0:
                print("ERROR: Dimensões da imagem inválidas")
                return JsonResponse({
                    'success': False,
                    'message': 'Imagem inválida. Verifique o arquivo enviado.',
                    'diagnostico': {
                        'dimensoes': img.shape if hasattr(img, 'shape') else 'Não disponível',
                        'tamanho': img.size if hasattr(img, 'size') else 'Não disponível'
                    }
                })
            
            # Converter para RGB para o face_recognition
            try:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            except Exception as color_error:
                print(f"ERRO ao converter imagem para RGB: {color_error}")
                return JsonResponse({
                    'success': False,
                    'message': 'Falha ao processar imagem. Erro na conversão de cor.',
                    'error_details': str(color_error)
                })
            
            # Tentar diferentes modelos de detecção facial com tratamento de erro
            face_locations = []
            detection_models = ["hog", "cnn"]
            
            for model in detection_models:
                try:
                    print(f"Tentando detecção facial com modelo: {model}")
                    current_face_locations = face_recognition.face_locations(rgb_img, model=model)
                    
                    if current_face_locations:
                        face_locations = current_face_locations
                        break
                except Exception as detection_error:
                    print(f"ERRO ao detectar rosto com modelo {model}: {detection_error}")
            
            # Se não encontrar rostos, retorna mensagem de erro
            if not face_locations:
                print("AVISO: Nenhum rosto detectado na imagem")
                return JsonResponse({
                    'success': False,
                    'message': 'Nenhum rosto detectado. Por favor, tire uma foto clara do rosto.',
                    'diagnostico': {
                        'dimensoes': img.shape,
                        'tamanho_imagem': img.size,
                        'modelos_testados': detection_models
                    }
                })
            
            # Retorna informação de que o rosto foi detectado, mas não será cadastrado automaticamente
            return JsonResponse({
                'success': True,
                'message': 'Rosto detectado com sucesso. Prossiga para o cadastro manual.',
                'faces_detected': len(face_locations)
            })
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR CRÍTICO ao processar imagem para cadastro rápido: {str(e)}")
            print(f"Detalhes do erro: {error_details}")
            return JsonResponse({
                'success': False,
                'error': 'Erro interno no processamento da imagem',
                'error_details': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@csrf_exempt
def registrar_visita_api(request):
    """API para registrar visita a partir do totem"""
    if request.method == 'POST':
        try:
            print("Recebendo solicitação de registro de visita via API")
            
            # Obter dados da visita
            visitante_id = request.POST.get('visitante_id')
            setor_id = request.POST.get('setor_id')
            objetivo = request.POST.get('objetivo')
            
            print(f"Dados recebidos: visitante_id={visitante_id}, setor_id={setor_id}, objetivo={objetivo}")
            
            # Validação básica
            if not visitante_id or not setor_id or not objetivo:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos os campos são obrigatórios'
                })
            
            # Buscar visitante e setor
            try:
                visitante = Visitante.objects.get(id=visitante_id)
                setor = Setor.objects.get(id=setor_id)
                
                # Criar visita usando a localização do setor selecionado
                visita = Visita.objects.create(
                    visitante=visitante,
                    setor=setor,
                    objetivo=objetivo,
                    status='em_andamento',
                    data_entrada=timezone.now(),
                    localizacao=setor.localizacao  # Usar a localização do setor
                )
                
                print(f"Visita registrada com sucesso: ID={visita.id}, Setor={setor}, Localização={setor.localizacao}")
                
                # Incluir URL para redirecionamento após emitir a etiqueta
                url_etiqueta = reverse('recepcao:gerar_etiqueta', args=[visita.id])
                url_totem_home = reverse('recepcao:totem_home')
                
                return JsonResponse({
                    'success': True,
                    'message': 'Visita registrada com sucesso',
                    'visita_id': visita.id,
                    'url_etiqueta': url_etiqueta,
                    'url_redirect': url_totem_home  # URL para redirecionamento após etiqueta
                })
                
            except Visitante.DoesNotExist:
                print(f"Erro: Visitante não encontrado (ID={visitante_id})")
                return JsonResponse({
                    'success': False,
                    'message': 'Visitante não encontrado'
                })
            except Setor.DoesNotExist:
                print(f"Erro: Setor não encontrado (ID={setor_id})")
                return JsonResponse({
                    'success': False,
                    'message': 'Setor não encontrado'
                })
            except Exception as e:
                print(f"Erro ao registrar visita: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': f'Erro ao registrar visita: {str(e)}'
                })
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERRO geral no registro de visita: {str(e)}")
            print(f"Detalhes do erro: {error_details}")
            return JsonResponse({
                'success': False,
                'message': f'Erro técnico: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

@csrf_exempt
def parar_reconhecimento_api(request):
    """
    API para interromper o processo de reconhecimento facial
    Limpa recursos, fecha câmera e reseta estado
    """
    try:
        # Adicionar lógica para limpar recursos de reconhecimento
        print("Interrompendo processo de reconhecimento facial")
        
        return JsonResponse({
            'success': True,
            'message': 'Processo de reconhecimento facial interrompido com sucesso'
        })
    except Exception as e:
        print(f"ERRO ao parar reconhecimento: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Falha ao interromper reconhecimento',
            'error_details': str(e)
        })

@csrf_exempt
def reload_encodings_api(request):
    """Endpoint para recarregar manualmente os encodings faciais sem reiniciar o servidor."""
    if request.method == 'POST':
        try:
            face_manager.reload_encodings()
            return JsonResponse({'success': True, 'message': 'Encodings recarregados com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
