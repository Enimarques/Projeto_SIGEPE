# Instalação Rápida do SIGEPE (Windows)

## 1. Pré-requisitos

- **Windows 10 ou 11**
- **Python 3.9+** (recomendado: 3.13.2)
- **Git**
- **Visual Studio Build Tools 2022**  
  - [Baixe aqui](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Marque a opção **"Desenvolvimento para desktop com C++"** na instalação

## 2. Baixe o Projeto

Abra o **Prompt de Comando** ou **PowerShell** e execute:

```sh
git clone https://github.com/seu-usuario/SIGEPE.git
cd SIGEPE
```

## 3. Crie e Ative o Ambiente Virtual

```sh
python -m venv venv
venv\Scripts\activate
```
pip install -r requirements.txt



## 4. Instale as Dependências

Execute o script de instalação:

```sh
instalar.bat
```

- **Opção 1**: Instalação Completa (com reconhecimento facial)
- **Opção 2**: Instalação Básica (sem reconhecimento facial)

O script irá:
- Verificar pré-requisitos
- Instalar todas as dependências (inclusive reconhecimento facial, se escolhido)
- Configurar o banco de dados

## 5. Inicialize o Sistema

```sh
iniciar.bat
```

- O servidor será iniciado e o sistema estará disponível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 6. Primeiros Passos

- Acesse o sistema com o superusuário criado durante a instalação.
- Para acessar o admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## 7. Solução de Problemas

- Se ocorrer erro de compilação, **reinstale o Visual Studio Build Tools** e reinicie o PC.
- Se faltar alguma dependência, execute novamente `instalar.bat`.
- Para checar requisitos, use:  
  ```sh
  verificar_requisitos.bat
  ```

---

**Pronto! O SIGEPE estará rodando no seu Windows.**
