# Scripts de Instalação e Execução do SIGEPE

Esta pasta contém scripts para automatizar a instalação e a execução do sistema SIGEPE no ambiente Windows.

## Instalação Rápida

Execute o script `instalar.bat`. Ele irá guiar você pelo processo.

Durante a execução, você poderá escolher entre dois modos de instalação:

### 1. Instalação **Completa** (com Reconhecimento Facial)
- Instala **todas** as funcionalidades do sistema, incluindo o totem de autoatendimento com reconhecimento facial.
- **Pré-requisito Obrigatório:** Requer o **Visual Studio Build Tools** com o pacote **"Desenvolvimento para desktop com C++"** instalado na máquina.
  - [Link para download](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Se este pré-requisito não for atendido, a instalação falhará.

### 2. Instalação **Básica** (sem Reconhecimento Facial)
- Instala o sistema com todas as funcionalidades, **exceto** as que dependem de reconhecimento facial.
- É a opção mais rápida e recomendada se você não precisa da funcionalidade de totem ou biometria.
- Não possui pré-requisitos complexos.

---

## Detalhes dos Scripts

### `instalar.bat`
Script principal que automatiza todo o setup:
1.  Verifica se o Python 3.9+ está instalado.
2.  Apresenta o menu para escolher entre a instalação Completa ou Básica.
3.  Exibe um aviso sobre os pré-requisitos da instalação Completa.
4.  Cria um ambiente virtual (`venv`) isolado para o projeto.
5.  Instala as dependências necessárias a partir do arquivo `requirements.txt` (Completa) ou `requirements-basic.txt` (Básica).
6.  Executa as migrações do banco de dados (`manage.py migrate`).
7.  Ao final, oferece a opção de criar um superusuário (admin).

### `iniciar.bat`
Inicia o servidor de desenvolvimento do Django:
1.  Ativa o ambiente virtual.
2.  Inicia o servidor na porta 8000.
3.  O sistema estará acessível em `http://127.0.0.1:8000`.

---

## Solução de Problemas

- **Erro na Instalação Completa:** Quase sempre o problema é a falta do **Visual Studio Build Tools** ou do pacote C++. Verifique a instalação, reinicie o terminal e tente executar `instalar.bat` novamente.
- **Python não encontrado:** Certifique-se de que o Python 3.9+ foi instalado e que a opção "Add Python to PATH" foi marcada durante a instalação.

## Versões das Dependências

- Python: 3.9 ou superior (testado com 3.13.2)
- Django: 5.0 ou superior
- Pillow: 9.5.0 ou superior
- numpy: 1.26.0 ou superior
