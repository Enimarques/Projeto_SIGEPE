# Dicas de Performance para Reconhecimento Facial com face_recognition

Estas dicas são baseadas na documentação oficial e discussões do repositório do [face_recognition](https://github.com/ageitgey/face_recognition), focadas em garantir performance e evitar travamentos na página do cliente em sistemas web.

---

## 1. Reduza a Resolução das Imagens
- Imagens grandes = processamento lento.
- Antes de enviar a imagem para o backend, redimensione para algo como **640x480** ou até menor, se possível.
- No frontend (JavaScript), use o canvas para redimensionar a imagem capturada da webcam antes de enviar.
- No backend, sempre processe imagens menores para acelerar a detecção e o encoding.

## 2. Evite Processar no Cliente
- O processamento facial deve ser feito no servidor, nunca no navegador do usuário.
- O cliente só deve capturar e enviar a imagem (já redimensionada).

## 3. Use Cache de Encodings
- Não gere encodings toda vez que for comparar.
- Gere e salve o encoding do rosto do visitante no momento do cadastro (no banco de dados ou arquivo).
- No reconhecimento, carregue todos os encodings já prontos e compare apenas os vetores (muito mais rápido).

## 4. Paralelize no Backend
- O `face_recognition` usa apenas 1 core por padrão.
- Se precisar comparar com muitos rostos, use Python `multiprocessing` para dividir a busca entre vários processos.
- Exemplo: se o servidor tem 4 núcleos, divida a lista de encodings em 4 partes e processe em paralelo.

## 5. Ajuste a Tolerância
- O parâmetro `tolerance` do `compare_faces` pode ser ajustado para evitar falsos positivos e acelerar a decisão.
- Valores menores tornam a comparação mais estrita (padrão é 0.6).

## 6. Evite Recarregar Encodings
- Carregue os encodings dos visitantes uma vez só (ex: ao iniciar o servidor ou ao cadastrar um novo visitante).
- Não recalcule ou recarregue do disco a cada requisição.

## 7. Use Hardware Adequado
- Se possível, use servidores com CPUs modernas (com AVX/SSE4) ou GPU (CUDA) para acelerar o dlib.
- Em ambientes Linux, a performance é melhor que em Windows/VMs.

## 8. Limite o Número de Comparações
- Se o número de visitantes for muito grande, use técnicas de pré-filtragem (ex: por setor, horário, etc) para reduzir o número de comparações por requisição.

## 9. Evite Virtualização Lenta
- Evite rodar o backend em máquinas virtuais lentas (ex: VirtualBox). Prefira Docker, VMs otimizadas ou bare metal.

---

## Exemplo de Redimensionamento no Frontend (JS)
```js
function resizeImage(image, width, height) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(image, 0, 0, width, height);
  return canvas.toDataURL('image/jpeg', 0.8);
}
```
Use isso antes de enviar a imagem para o backend.

---

## Resumo Prático para Projetos Web
- **No frontend:** Redimensione a imagem antes de enviar e mostre feedback de "processando".
- **No backend:** Salve encodings prontos, compare apenas encodings, use multiprocessing e cache.
- **Infraestrutura:** Use servidores Linux e CPUs modernas. Considere GPU se o volume crescer muito.

---

Essas dicas vão garantir que a página do cliente não trave e o reconhecimento facial seja rápido e confiável. 