import cv2
import face_recognition

# Teste simples para verificar se as bibliotecas estão funcionando
def test_face_libraries():
    print("OpenCV version:", cv2.__version__)
    print("face_recognition is available")
    
    # Tenta inicializar a câmera
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("Camera is accessible")
            ret, frame = cap.read()
            if ret:
                print("Successfully captured a frame")
                # Tenta detectar rostos no frame
                face_locations = face_recognition.face_locations(frame)
                print(f"Detected {len(face_locations)} faces in test frame")
            cap.release()
        else:
            print("Camera is not accessible")
    except Exception as e:
        print("Error testing camera:", str(e))

if __name__ == "__main__":
    test_face_libraries()
