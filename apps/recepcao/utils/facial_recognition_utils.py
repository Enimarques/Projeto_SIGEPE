import face_recognition
import numpy as np

def get_face_embedding(image_file):
    """
    Carrega uma imagem e retorna o embedding facial da primeira face encontrada.

    Args:
        image_file: Um objeto de arquivo de imagem (como de um request.FILES).

    Returns:
        Uma lista de 128 floats representando o embedding facial, 
        ou None se nenhuma face for encontrada.
        
    Raises:
        ValueError: Se mais de uma face for encontrada na imagem.
    """
    try:
        # Resetar o ponteiro do arquivo para o início
        image_file.seek(0)
        # Carrega a imagem a partir do objeto de arquivo em memória
        image = face_recognition.load_image_file(image_file)
        
        # Gera os embeddings faciais para todas as faces na imagem
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            # Nenhuma face encontrada
            return None
        elif len(face_encodings) > 1:
            # Mais de uma face encontrada, o que é um erro para fotos de cadastro
            raise ValueError("Mais de uma face foi detectada na imagem.")
        else:
            # Retorna o embedding da única face encontrada, convertido para uma lista Python
            return face_encodings[0].tolist()
            
    except Exception as e:
        # Em caso de qualquer outro erro na biblioteca (ex: formato de imagem inválido)
        # logamos o erro e retornamos None ou relançamos a exceção.
        # Por enquanto, vamos relançar para ter mais detalhes durante o desenvolvimento.
        print(f"Erro ao processar a imagem para reconhecimento facial: {e}")
        raise 