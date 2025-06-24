# Arquitetura Técnica do Modo Totem

A implementação do Modo Totem segue uma arquitetura cliente-servidor, onde o frontend (rodando no navegador do totem) se comunica com o backend (Django) através de APIs REST.

## Frontend

O frontend é composto por uma série de templates HTML, estilizados com CSS e controlados por JavaScript.

-   **Templates:**
    -   `base_totem.html`: Template base que inclui os arquivos estáticos (CSS, JS) e define a estrutura principal da interface do totem.
    -   `totem_identificacao.html`: A página inicial que contém o elemento `<video>` para a câmera e carrega a lógica de reconhecimento facial.
    -   `totem_destino.html`: Apresenta os botões de seleção de destino e contém o script para registrar a visita.
    -   `totem_comprovante.html`: Exibe o comprovante final da visita e os botões de ação (Imprimir, Finalizar).

-   **JavaScript (`static/js/camera.js`):**
    -   É o cérebro do lado do cliente.
    -   Responsável por inicializar a câmera do dispositivo via `navigator.mediaDevices.getUserMedia`.
    -   Carrega os modelos da `face-api.js` para detecção de rosto.
    -   Executa um loop contínuo (`setInterval`) para analisar os frames do vídeo, detectar rostos e enviar a imagem para o backend.
    -   Manipula as respostas da API e redireciona o usuário entre as diferentes telas do fluxo.

-   **CSS (`static/css/style.css`):**
    -   Contém todas as regras de estilo para garantir que a interface do totem seja limpa, legível e fácil de usar em uma tela de toque.
    -   Inclui regras específicas para impressão (`@media print`) para formatar corretamente a etiqueta/comprovante.

## Backend (Django)

O backend gerencia a lógica de negócio, a interação com o banco de dados e expõe os endpoints necessários para o frontend.

-   **Views (`apps/recepcao/views.py`):**
    -   `totem_identificacao`: Renderiza o template inicial.
    -   `totem_destino`: Renderiza a tela de seleção de destino, passando os dados do visitante reconhecido.
    -   `totem_comprovante`: Busca os dados de uma visita específica pelo ID e renderiza a página do comprovante.
    -   `api_find_person_by_face`: Um endpoint de API que recebe uma imagem (em Base64), a converte, e usa a lógica de reconhecimento facial para encontrar um `Visitante` correspondente no banco de dados. Retorna os dados do visitante em formato JSON.
    -   `api_registrar_visita_totem`: Endpoint que recebe a ID do visitante e do destino, cria o registro da `Visita` e retorna o ID da nova visita.

-   **URLs (`apps/recepcao/urls.py`):**
    -   Mapeia as URLs (ex: `/totem/identificacao/`, `/api/registrar-visita/`) para as suas respectivas views no Django.

-   **Models (`apps/recepcao/models.py`):**
    -   `Visitante`: Armazena os dados cadastrais dos visitantes, incluindo o `biometric_vector` usado para o reconhecimento facial.
    -   `Visita`: Registra cada evento de visita, vinculando um `Visitante` a um `Setor` (destino) em uma data/hora específica. 