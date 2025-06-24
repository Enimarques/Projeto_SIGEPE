# Detalhes do Reconhecimento Facial

O reconhecimento facial é a tecnologia central do Modo Totem. A implementação é dividida entre o frontend (para detecção rápida) e o backend (para comparação e identificação).

## Frontend: Detecção com `face-api.js`

-   **Biblioteca:** Utilizamos a `face-api.js`, uma biblioteca JavaScript que roda diretamente no navegador, construída sobre o TensorFlow.js.
-   **Propósito:** A principal responsabilidade no frontend é a **detecção**, ou seja, encontrar *se* e *onde* há um rosto no feed de vídeo. Isso é feito localmente no navegador para ser rápido e não sobrecarregar o servidor com um fluxo de vídeo contínuo.
-   **Processo:**
    1.  **Carregamento dos Modelos:** Ao iniciar, o `camera.js` carrega modelos pré-treinados da `face-api.js` para detecção de rostos.
    2.  **Análise de Vídeo:** A cada poucos milissegundos, um frame do vídeo é capturado em um canvas HTML.
    3.  **Detecção:** A `face-api.js` processa a imagem do canvas para localizar um rosto.
    4.  **Captura e Envio:** Uma vez que um rosto é detectado com confiança, a imagem desse rosto é recortada, convertida para o formato Base64 e enviada para a API do nosso backend.

## Backend: Identificação com `face_recognition`

-   **Biblioteca:** Usamos a biblioteca Python `face_recognition`, que é um wrapper de alto nível para a poderosa biblioteca `dlib`.
-   **Propósito:** A responsabilidade do backend é a **identificação**. Ele recebe a imagem de um rosto detectado e deve descobrir *a quem* esse rosto pertence.
-   **Processo:**
    1.  **Geração de Vetor (Cadastro):** Quando um novo visitante é cadastrado no sistema com uma foto, o `face_recognition` é usado para analisar a foto, localizar o rosto e gerar um **vetor biométrico** (uma lista de 128 números que representa as características únicas daquele rosto). Esse vetor é salvo no campo `biometric_vector` do modelo `Visitante`.
    2.  **Comparação (Totem):**
        -   A API `api_find_person_by_face` recebe a imagem do totem.
        -   Ela gera o vetor biométrico para o rosto recebido.
        -   Em seguida, ela compara esse novo vetor com **todos** os vetores biométricos armazenados no banco de dados.
        -   A comparação calcula a "distância" euclidiana entre os vetores. Uma distância menor significa rostos mais parecidos.
        -   Se a menor distância encontrada estiver abaixo de um limiar de tolerância (geralmente ~0.6), o sistema considera uma correspondência e identifica o visitante.
        -   Os dados do visitante correspondente são então retornados em formato JSON para o frontend. 