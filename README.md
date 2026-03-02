# SIGEPE - Sistema de Gestão de Pessoas e Veículos

## Índice
1. [Visão Geral](#visao-geral)
2. [Pré-requisitos](#pre-requisitos)
3. [Instalação no Linux](#instalacao-linux)
4. [Configuração do Ambiente](#configuracao-ambiente)
5. [Instalação de Dependências](#instalacao-dependencias)
6. [Configuração do Banco de Dados](#configuracao-banco)
7. [Configuração do Gunicorn e Nginx](#gunicorn-nginx)
8. [Iniciando o Serviço](#iniciando-servico)
9. [Módulos e Funcionalidades](#modulos)
10. [Fluxos Principais](#fluxos)
11. [Endpoints Principais](#endpoints)
12. [Administração e Segurança](#administracao)
13. [Solução de Problemas](#solucao)
14. [Documentação Extra](#documentacao-extra)

---

## 1. Visão Geral <a name="visao-geral"></a>
O SIGEPE é um sistema modular para controle de visitantes, veículos, departamentos, gabinetes e autoatendimento (totem), com interface web moderna, relatórios, reconhecimento facial (opcional) e recursos de acessibilidade.

---

## 2. Pré-requisitos <a name="pre-requisitos"></a>

- Sistema operacional baseado em Linux (Ubuntu 20.04/22.04 recomendado)
- Python 3.10+
- pip (gerenciador de pacotes Python)
- Git
- CMake 3.18+
- Compiladores C++
- Bibliotecas de desenvolvimento
- Nginx (para produção)
- Gunicorn (servidor WSGI)
- Supervisor (opcional, para gerenciamento de processos)

## 3. Instalação no Linux <a name="instalacao-linux"></a>

### 3.1 Atualize o sistema e instale pacotes básicos

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential cmake git python3-pip python3-venv libsm6 libxext6 libxrender-dev libgl1-mesa-glx
```

### 3.2 Instale o CMake (se ainda não estiver instalado)

```bash
sudo apt install -y cmake
```

## 4. Configuração do Ambiente <a name="configuracao-ambiente"></a>

### 4.1 Clone o repositório

```bash
cd /opt
sudo git clone https://github.com/TersanPlay/Urutal.git ProjetoSigepe
sudo chown -R $USER:$USER /opt/ProjetoSigepe
cd ProjetoSigepe
```

### 4.2 Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. Instalação de Dependências <a name="instalacao-dependencias"></a>

### 5.1 Instale todas as dependências do sistema de uma vez

```bash
# Atualize a lista de pacotes
sudo apt update

# Instale todas as dependências do sistema necessárias
sudo apt install -y \
    build-essential \
    cmake \
    git \
    python3-pip \
    python3-venv \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    python3-dev \
    libopenblas-dev \
    libatlas-base-dev \
    liblapack-dev \
    gfortran \
    nginx
```

### 5.2 Instale todas as dependências do Python

```bash
# Atualize o pip
pip install --upgrade pip

# Instale todas as dependências do Python
pip install -r requirements.txt
```

### 5.3 Verificação da instalação

Verifique se as principais dependências foram instaladas corretamente:

```bash
python -c "import dlib; print(f'dlib version: {dlib.__version__}')"
python -c "import face_recognition; print('face_recognition importado com sucesso')"
python -c "import pandas as pd; print(f'pandas version: {pd.__version__}')"
```

## 6. Configuração do Banco de Dados <a name="configuracao-banco"></a>

### 6.1 Aplique as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 6.3 Colete arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

## 7. Configuração do Gunicorn e Nginx <a name="gunicorn-nginx"></a>

### 7.1 Instale o Gunicorn

```bash
pip install gunicorn
```

### 7.2 Crie um arquivo de configuração do Gunicorn

Crie um arquivo `gunicorn.service` em `/etc/systemd/system/` com o seguinte conteúdo:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=administrator
Group=www-data
WorkingDirectory=/opt/ProjetoSigepe
ExecStart=/opt/ProjetoSigepe/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/opt/ProjetoSigepe/sigepe.sock SIGEPE.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 7.3 Instale e configure o Nginx

```bash
sudo apt install -y nginx
```

Crie um arquivo de configuração em `/etc/nginx/sites-available/sigepe`:

```nginx
server {
    listen 80;
    server_name seu_dominio_ou_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /opt/ProjetoSigepe;
    }

    location /media/ {
        root /opt/ProjetoSigepe;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/ProjetoSigepe/sigepe.sock;
    }
}
```

Ative o site e reinicie o Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/sigepe /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 8. Iniciando o Serviço <a name="iniciando-servico"></a>

### 8.1 Inicie e habilite o serviço do Gunicorn

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 8.2 Verifique o status do serviço

```bash
sudo systemctl status gunicorn
```

### 8.3 Acesse a aplicação

Acesse o endereço IP do seu servidor ou domínio configurado no navegador:

```
http://seu_dominio_ou_ip/
```

### 8.4 Gerenciando o serviço

- Para reiniciar o serviço:
  ```bash
  sudo systemctl restart gunicorn
  ```

- Para ver os logs:
  ```bash
  sudo journalctl -u gunicorn
  ```

---

## 9. Módulos e Funcionalidades <a name="modulos"></a>

- **Veículos:** Cadastro, controle de entrada/saída, relatórios, busca, status.
- **Visitantes:** Cadastro, validação de CPF, upload de foto, histórico de visitas.
- **Recepção:** Painel de estatísticas, registro de visitas, ações rápidas.
- **Totem:** Autoatendimento, reconhecimento facial, comprovante digital e impressão.
- **Departamentos:** Cadastro, cards informativos, integração com visitas.
- **Gabinetes:** Cadastro, cards informativos, integração com visitas.
- **Relatórios:** Exportação em PDF, filtros avançados.
- **Acessibilidade:** Contraste, navegação por teclado, responsividade.

---

## 10. Fluxos Principais <a name="fluxos"></a>

- **Cadastro de Veículo:** `/veiculos/registro-entrada/`
- **Saída de Veículo:** `/veiculos/registro-saida/`
- **Cadastro de Visitante:** `/recepcao/cadastro-visitantes/`
- **Registro de Visita:** `/recepcao/registro-visitas/`
- **Autoatendimento Totem:** `/recepcao/totem/welcome/` → reconhecimento facial → seleção de destino → comprovante

---

## 11. Endpoints Principais <a name="endpoints"></a>

- `/veiculos/` — Lista de veículos
- `/recepcao/visitantes/` — Lista de visitantes
- `/recepcao/registro-visitas/` — Registro de visitas
- `/recepcao/totem/identificacao/` — Início do totem
- `/recepcao/totem/destino/` — Seleção de destino no totem
- `/recepcao/totem/comprovante/<id>/` — Comprovante de visita

---

## 12. Administração e Segurança <a name="administracao"></a>

- Interface administrativa: `/admin/`
- Controle de permissões por grupo
- Validação de dados no cliente e servidor
- Proteção contra dados duplicados
- Logs de alterações e auditoria

---

## 13. Solução de Problemas <a name="solucao"></a>

### 13.1 Erros comuns e soluções

**Problema:** Erro ao instalar as dependências
```
ERROR: Failed building wheel for [pacote]
```
**Solução:** Certifique-se de que todas as dependências de sistema foram instaladas corretamente. Use o comando de instalação completo:
```bash
sudo apt update && sudo apt install -y build-essential cmake git python3-pip python3-venv libsm6 libxext6 libxrender-dev libgl1-mesa-glx python3-dev libopenblas-dev libatlas-base-dev liblapack-dev gfortran nginx
```

**Problema:** Erro ao instalar o dlib
```
ERROR: Failed building wheel for dlib
```
**Solução:** Certifique-se de que todas as dependências de desenvolvimento estão instaladas:
```bash
sudo apt install -y build-essential cmake python3-dev python3-pip libopenblas-dev libatlas-base-dev liblapack-dev
```

**Problema:** Erro de permissão ao acessar o socket do Gunicorn
```
connect() to unix:/opt/ProjetoSigepe/sigepe.sock failed (13: Permission denied)
```
**Solução:** Ajuste as permissões do diretório e do socket:
```bash
sudo chown -R administrator:www-data /opt/ProjetoSigepe
sudo chmod -R 775 /opt/ProjetoSigepe
```

**Problema:** Erro ao importar módulos Python
```
ModuleNotFoundError: No module named 'nome_do_modulo'
```
**Solução:** Instale o módulo faltante:
```bash
source /opt/ProjetoSigepe/venv/bin/activate
pip install nome_do_modulo
```

### 13.2 Verificação de logs

- Logs do Gunicorn:
  ```bash
  sudo journalctl -u gunicorn -n 100 -f
  ```

- Logs do Nginx:
  ```bash
  sudo tail -f /var/log/nginx/error.log
  sudo tail -f /var/log/nginx/access.log
  ```

- **Erro de compilação:** Reinstale o Visual Studio Build Tools e reinicie o PC.
- **Dependências:** Execute novamente `instalar.bat`.
- **Requisitos:** Use `verificar_requisitos.bat`.
- **Resetar senha admin:** Use o script `set_password.py`.

---

## 14. Documentação Extra <a name="documentacao-extra"></a>

- **`requirements.txt`**: Contém todas as dependências do Python necessárias para o projeto, incluindo versões específicas para garantir compatibilidade e comentários úteis para instalação.
- **Documentação detalhada** de fluxos, permissões, relatórios e integrações está disponível na pasta `/docs/`.
- **Scripts utilitários** para manutenção estão em `/scripts/` ou na raiz do projeto.

### Gerenciamento de Dependências

Para atualizar as dependências:
1. Instale/atualize os pacotes necessários
2. Atualize o `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```
3. Se necessário, edite o arquivo para manter os comentários úteis

### Dependências de Desenvolvimento

Para desenvolvimento, instale também:
```bash
pip install black flake8 isort pre-commit
```

---

**Pronto! O SIGEPE estará rodando no seu Windows. Para dúvidas ou contribuições, consulte a documentação extra ou entre em contato com o mantenedor do projeto.**
