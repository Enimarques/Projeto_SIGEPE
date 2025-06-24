# Fluxo de Uso do Totem

O fluxo de interação do visitante com o totem foi projetado para ser o mais simples e direto possível.

1.  **Início e Ativação da Câmera (`totem_identificacao.html`)**
    -   O visitante se posiciona em frente ao totem.
    -   A página inicial é exibida, e a câmera é ativada automaticamente, iniciando a busca por um rosto.

2.  **Reconhecimento Facial**
    -   O script `camera.js` analisa o feed de vídeo em tempo real usando a biblioteca `face-api.js`.
    -   Quando um rosto é detectado e atinge um limiar mínimo de tamanho na tela (garantindo uma boa captura), a imagem do rosto é enviada para a API de reconhecimento do backend.
    -   Se o visitante é reconhecido, o sistema o redireciona para a próxima etapa.

3.  **Seleção de Destino (`totem_destino.html`)**
    -   A tela exibe uma lista de possíveis destinos (ex: Gabinetes, Departamentos).
    -   O visitante toca no destino desejado.

4.  **Confirmação e Registro da Visita**
    -   Ao selecionar um destino, uma chamada de API (`api_registrar_visita_totem`) é feita para o backend, enviando a ID do visitante e a ID do destino.
    -   O backend cria um novo registro de `Visita` no banco de dados com o status "Aguardando".

5.  **Exibição do Comprovante (`totem_comprovante.html`)**
    -   Após o registro bem-sucedido, o navegador é redirecionado para a página do comprovante.
    -   A tela exibe os detalhes da visita: nome do visitante, foto, destino, data, hora e um QR Code único.

6.  **Ações Finais**
    -   O visitante tem duas opções:
        -   **Imprimir:** Aciona a função de impressão do navegador para gerar uma etiqueta física.
        -   **Finalizar:** Retorna o totem à tela inicial, pronto para o próximo visitante. 