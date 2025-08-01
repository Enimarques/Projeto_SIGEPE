# SIGEPE - Sistema de Gestão de Pessoas e Veículos

## Índice
1. [Visão Geral](#visao-geral)
2. [Instalação Rápida (Windows)](#instalacao-rapida)
3. [Módulos e Funcionalidades](#modulos)
4. [Fluxos Principais](#fluxos)
5. [Endpoints Principais](#endpoints)
6. [Administração e Segurança](#administracao)
7. [Solução de Problemas](#solucao)
8. [Documentação Extra](#documentacao-extra)

---

## 1. Visão Geral <a name="visao-geral"></a>
O SIGEPE é um sistema modular para controle de visitantes, veículos, departamentos, gabinetes e autoatendimento (totem), com interface web moderna, relatórios, reconhecimento facial (opcional) e recursos de acessibilidade.

---

## 2. Instalação Rápida (Windows) <a name="instalacao-rapida"></a>

### Pré-requisitos
- Windows 10 ou 11
- Python 3.9+
- Git
- Visual Studio Build Tools 2022 (com C++)
- cmake

### Passos

```sh
git clone https://github.com/seu-usuario/SIGEPE.git
cd SIGEPE
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
instalar.bat
```
- Siga as opções do instalador para instalação completa (com reconhecimento facial) ou básica.
- Para iniciar:
  ```sh
  iniciar.bat
  ```
  Ou manualmente:
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 3. Módulos e Funcionalidades <a name="modulos"></a>

- **Veículos:** Cadastro, controle de entrada/saída, relatórios, busca, status.
- **Visitantes:** Cadastro, validação de CPF, upload de foto, histórico de visitas.
- **Recepção:** Painel de estatísticas, registro de visitas, ações rápidas.
- **Totem:** Autoatendimento, reconhecimento facial, comprovante digital e impressão.
- **Departamentos:** Cadastro, cards informativos, integração com visitas.
- **Gabinetes:** Cadastro, cards informativos, integração com visitas.
- **Relatórios:** Exportação em PDF, filtros avançados.
- **Acessibilidade:** Contraste, navegação por teclado, responsividade.

---

## 4. Fluxos Principais <a name="fluxos"></a>

- **Cadastro de Veículo:** `/veiculos/registro-entrada/`
- **Saída de Veículo:** `/veiculos/registro-saida/`
- **Cadastro de Visitante:** `/recepcao/cadastro-visitantes/`
- **Registro de Visita:** `/recepcao/registro-visitas/`
- **Autoatendimento Totem:** `/recepcao/totem/welcome/` → reconhecimento facial → seleção de destino → comprovante

---

## 5. Endpoints Principais <a name="endpoints"></a>

- `/veiculos/` — Lista de veículos
- `/recepcao/visitantes/` — Lista de visitantes
- `/recepcao/registro-visitas/` — Registro de visitas
- `/recepcao/totem/identificacao/` — Início do totem
- `/recepcao/totem/destino/` — Seleção de destino no totem
- `/recepcao/totem/comprovante/<id>/` — Comprovante de visita

---

## 6. Administração e Segurança <a name="administracao"></a>

- Interface administrativa: `/admin/`
- Controle de permissões por grupo
- Validação de dados no cliente e servidor
- Proteção contra dados duplicados
- Logs de alterações e auditoria

---

## 7. Solução de Problemas <a name="solucao"></a>

- **Erro de compilação:** Reinstale o Visual Studio Build Tools e reinicie o PC.
- **Dependências:** Execute novamente `instalar.bat`.
- **Requisitos:** Use `verificar_requisitos.bat`.
- **Resetar senha admin:** Use o script `set_password.py`.

---

## 8. Documentação Extra <a name="documentacao-extra"></a>

- Documentação detalhada de fluxos, permissões, relatórios e integrações está disponível na pasta `/docs/`.
- Scripts utilitários para manutenção estão em `/scripts/` ou na raiz do projeto.

---

**Pronto! O SIGEPE estará rodando no seu Windows. Para dúvidas ou contribuições, consulte a documentação extra ou entre em contato com o mantenedor do projeto.**
