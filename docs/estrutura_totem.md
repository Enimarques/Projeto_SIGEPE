# Estrutura das Páginas do Totem de Visitas

## 1. Página `/recepcao/totem/`

### Objetivo
Interface de totem para identificação de visitantes via reconhecimento facial, com experiência otimizada para uso em quiosques.

### Estrutura HTML
- **Botão Voltar para Recepção**: Fora do card, alinhado à direita, sobre o fundo cinza claro.
- **Card Central Branco**: Contém título, área de vídeo, mensagens e botões.
- **Área de Vídeo**: Mostra a câmera do usuário, com guia oval amarelo para posicionamento do rosto.
- **Mensagens de Status**: Feedback visual sobre o processo.
- **Botões**:
  - Reiniciar Câmera
  - Iniciar Reconhecimento (só ativa o reconhecimento facial ao clicar)

### Fluxo JS
- Ao carregar, ativa a câmera.
- Só inicia o reconhecimento facial ao clicar em "Iniciar Reconhecimento".
- Envia frames para o backend apenas quando solicitado.
- Mostra modal de sucesso ao reconhecer, ou mensagens de erro caso não detecte rosto.

### CSS
- Layout responsivo, card centralizado, área de vídeo com borda azul e guia oval amarelo.
- Botões coloridos, acessíveis e com ícones.

### Integração Backend
- **Endpoint `/recepcao/api/verificar-face/`**: Recebe imagem, retorna se o rosto foi reconhecido e dados do visitante.
- **Endpoint `/recepcao/api/cadastro-rapido/`**: Cadastra rosto não reconhecido para posterior registro.
- **Redirecionamento**: Após sucesso, avança para `/recepcao/totem/setor/?visitante_id=...`.

---

## 2. Página `/recepcao/totem/setor/`

### Objetivo
Permitir ao visitante reconhecido escolher o setor/gabinete para registrar sua visita.

### Estrutura HTML
- **Card Central**: Exibe dados do visitante (nome, foto, documento).
- **Lista de Setores/Gabinetes**: Botões ou cards para seleção.
- **Botão Confirmar Visita**: Finaliza o registro da visita.

### Fluxo JS
- Recebe o visitante_id via query string.
- Exibe dados do visitante e opções de setor/gabinete.
- Ao selecionar e confirmar, envia para o backend registrar a visita.

### Integração Backend
- **Endpoint para buscar dados do visitante**: Recebe visitante_id, retorna dados pessoais e foto.
- **Endpoint para registrar visita**: Recebe visitante_id e setor/gabinete, registra a visita.

---

## 3. Vinculação com Backend (Django)
- **Views**: Funções ou classes em `views.py` que renderizam os templates e processam as requisições AJAX/POST.
- **URLs**: Registradas em `urls.py` do app `recepcao`.
- **Templates**: Localizados em `templates/recepcao/totem.html` e `templates/recepcao/totem_setor.html`.
- **APIs**: Endpoints REST para reconhecimento facial e cadastro rápido.
- **Mensagens**: Retornos em JSON para o frontend exibir feedback ao usuário.

---

## 4. Fluxo Resumido
1. Visitante se posiciona no totem e clica em "Iniciar Reconhecimento".
2. Se reconhecido, modal de sucesso e avança para seleção de setor.
3. Se não reconhecido, mensagem de erro ou redirecionamento para cadastro.
4. Visitante seleciona setor/gabinete e confirma visita.
5. Backend registra a visita e exibe confirmação.

---

## 5. Arquivos Relacionados
- `templates/recepcao/totem.html`
- `templates/recepcao/totem_setor.html`
- `static/js/` (separação recomendada para JS customizado)
- `views.py` e `urls.py` do app `recepcao`
- Endpoints de API para reconhecimento/cadastro

---

> **Dica:** Para manutenção, mantenha o JS modular e os endpoints REST bem documentados. Use mensagens claras para o usuário e garanta responsividade e acessibilidade visual. 