# Configuração e Dependências

Para que o Modo Totem e o Reconhecimento Facial funcionem corretamente, é necessário garantir que todas as dependências estejam instaladas e configuradas.

## Dependências de Backend (Python)

Todas as bibliotecas Python necessárias estão listadas no arquivo `requirements.txt`. As mais críticas para esta funcionalidade são:

-   `Django`: O framework web principal.
-   `Pillow`: Para manipulação de imagens no backend.
-   `face-recognition`: A biblioteca principal para geração de vetores biométricos e comparação de rostos.
-   `numpy`: Requerido pelo `face-recognition` para operações matemáticas.
-   `dlib` e `cmake`: Dependências de baixo nível para o `face-recognition`. A instalação pode exigir compiladores C++ e ferramentas de build no sistema operacional.

A instalação é feita com o comando padrão:
`pip install -r requirements.txt`

## Dependências de Frontend (JavaScript)

As bibliotecas JavaScript não são gerenciadas por um pacote como o `npm`, mas sim incluídas diretamente nos templates.

-   **`face-api.js`:** A biblioteca de detecção facial. O arquivo `face-api.min.js` deve estar presente na pasta `static/js/` (ou similar) e ser incluído no `base_totem.html`.
-   **Modelos da `face-api.js`:** A biblioteca requer arquivos de modelos pré-treinados para funcionar. Esses arquivos (como `ssd_mobilenetv1_model-weights_manifest.json`, etc.) devem estar em uma pasta acessível publicamente (ex: `static/js/models/`) para que o `camera.js` possa carregá-los.

A inclusão no template `base_totem.html` se parece com:
```html
<script defer src="{% static 'js/face-api.min.js' %}"></script>
<script defer src="{% static 'js/camera.js' %}"></script>
```

## Configuração do Projeto

-   **Variáveis de Ambiente:** Nenhuma variável de ambiente específica é necessária apenas para o totem, mas a configuração geral do Django (como `SECRET_KEY`, `DEBUG`, etc.) deve estar presente.
-   **URLs:** As rotas do totem devem estar corretamente incluídas no arquivo `SIGEPE/urls.py` a partir do `apps/recepcao/urls.py`.
-   **Banco de Dados:** O banco de dados deve estar migrado (`python manage.py migrate`) para garantir que os modelos `Visitante` e `Visita` existam com todos os campos necessários. 