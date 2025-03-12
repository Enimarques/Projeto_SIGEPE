# SIGEPE - Sistema de Gestão de Pessoas e Veículos

## Índice
1. [Sistema de Veículos](#sistema-de-veículos)
2. [Interface Administrativa](#interface-administrativa)
3. [Validações e Segurança](#validações-e-segurança)
4. [Interface do Usuário](#interface-do-usuário)
5. [Sistema de Visitantes](#sistema-de-visitantes)
6. [Relatórios e Analytics](#relatórios-e-analytics)
7. [Integrações](#integrações)
8. [Automação e IoT](#automação-e-iot)
9. [Sustentabilidade](#sustentabilidade)
10. [Acessibilidade](#acessibilidade)
11. [Arquitetura e Organização](#arquitetura-e-organização)
12. [Melhorias Recentes](#melhorias-recentes)
13. [Roadmap de Desenvolvimento](#roadmap-de-desenvolvimento)
14. [Detalhes Técnicos](#detalhes-técnicos)
15. [Integrações e Padrões Específicos](#integrações-e-padrões-específicos)

## Sistema de Veículos

### Validação de Placas (10/03/2025)
- Implementado suporte para dois formatos de placas:
  - Formato antigo: ABC-1234
  - Formato Mercosul: ABC1D23
- Validação automática no modelo e formulário
- Conversão automática para maiúsculas
- Mensagens de erro personalizadas

### Sistema de Status (10/03/2025)
- Adicionado campo de status para veículos
- Opções disponíveis:
  - "Presente no Estacionamento"
  - "Saída Realizada"
- Atualização automática baseada no horário de saída
- Indicadores visuais com animações
- Interface responsiva e moderna

### Tipos de Veículos
- Categorias implementadas:
  - Carro
  - Moto
  - Caminhonete
  - Caminhão
  - Ônibus
  - Outros

### Cores de Veículos
- Padronização conforme DETRAN:
  - Amarela
  - Azul
  - Bege
  - Branca
  - Cinza
  - Dourada
  - Grená
  - Laranja
  - Marrom
  - Prata
  - Preta
  - Rosa
  - Roxa
  - Verde
  - Vermelha
  - Fantasia

## Interface Administrativa

### Melhorias Visuais (10/03/2025)
- Cores dos veículos com indicadores visuais
- Status com animações e efeitos:
  - Verde pulsante para veículos presentes
  - Vermelho para veículos que saíram
- Organização em seções lógicas
- Filtros e buscas aprimorados

### Campos Organizados (10/03/2025)
- Informações do Veículo
  - Placa
  - Modelo
  - Cor
  - Tipo
- Responsável (seção dedicada)
- Status e Horários
  - Entrada (automático)
  - Saída (opcional)
  - Status (automático)
- Observações (colapsável)

### Acesso Administrativo (12/03/2025)
- Credenciais de Acesso:
  - Usuário: admin
  - Senha: admin123
  - URL: http://localhost:8000/admin
- Observações:
  - Recomenda-se alterar a senha após o primeiro acesso
  - Acesso restrito apenas para administradores do sistema
  - Interface administrativa completa do Django

## Sistema de Visitantes

### Melhorias no Cadastro (10/03/2025)
- Objetivo da visita movido para o cadastro do visitante
- Campos obrigatórios:
  - Nome completo
  - CPF (único)
  - Telefone
  - Cidade
  - Objetivo da visita
- Campos opcionais:
  - Nome social
  - Email
  - Foto
  - Descrição (quando objetivo for "Outros")

### Registro de Visitas (10/03/2025)
- Simplificação do processo:
  - Seleção do visitante já cadastrado
  - Data e hora de entrada automáticas
  - Campo para observações
  - Registro de saída opcional
- Validações aprimoradas:
  - Visitante obrigatório
  - Verificação de dados completos
  - Prevenção de duplicatas

### Interface de Visitas (10/03/2025)
- Transformada em interface somente leitura:
  - Removido botão de adicionar visitas
  - Removidos botões de edição
  - Removidos botões de exclusão
  - Foco em consulta e visualização

- Criação automática de visitas:
  - Visita criada automaticamente ao cadastrar visitante
  - Data e hora registradas automaticamente
  - Vinculação automática com o visitante

- Melhorias visuais:
  - Nome do visitante em negrito
  - Nome social exibido quando disponível
  - Status coloridos e intuitivos:
    - Verde para visitas em andamento
    - Vermelho para visitas finalizadas
    - Alertas visuais para dados inconsistentes

- Funcionalidades de consulta:
  - Busca por nome, nome social ou CPF
  - Filtros por objetivo, data e status
  - Ordenação por todas as colunas
  - Exibição clara de datas e horários

- Informações exibidas:
  - Nome completo do visitante
  - Objetivo da visita (com detalhes para "Outros")
  - Data e hora da visita
  - Status da visita
  - Horário de saída (quando aplicável)

### Objetivos de Visita
- Opções padronizadas:
  - Reunião com o Vereador
  - Discussão de Projetos de Lei
  - Apoio a Proposta de Lei
  - Solicitação de Auxílio
  - Apresentação de Projeto
  - Pedido de Apoio Social
  - Audiência Pública
  - Assinatura de Documentos
  - Visita Institucional
  - Reunião com Assessoria
  - Denúncias ou Reclamações
  - Eventos e Comemorações
  - Visita a Obras
  - Entrevista
  - Acompanhamento de Demandas
  - Entrega de Documentos
  - Consultoria Jurídica
  - Outros (com descrição)

## Validações e Segurança

### Validações de Formulário (10/03/2025)
- Validação de placas em tempo real
- Campos obrigatórios claramente marcados
- Feedback visual imediato
- Prevenção de dados duplicados
- Validação de CPF único
- Validação de objetivos de visita
- Verificação de datas e horários

### Segurança
- Proteção contra submissão de dados inválidos
- Validação tanto no cliente quanto no servidor
- Campos protegidos contra edição indevida
- Registro de alterações (log de mudanças)

## Interface do Usuário

### Melhorias Visuais (10/03/2025)
- Sistema de grid para seleção de cores
- Indicadores de status animados
- Cards responsivos para lista de veículos
- Efeitos de hover e transições suaves
- Ícones intuitivos para status
- Cores semânticas para feedback

## Detalhes Técnicos (12/03/2025)

### Stack Tecnológico
- Backend:
  - Django 4.2.0+: Framework web principal
  - Python 3.8+: Linguagem base
  - SQLite: Banco de dados em desenvolvimento
- Frontend:
  - HTML5/CSS3: Estrutura e estilização
  - JavaScript: Interatividade
  - django-widget-tweaks 1.4.12+: Customização de formulários
- Processamento de Imagens:
  - Pillow 9.5.0+: Manipulação de fotos de visitantes

### Configurações Django
- Configurações Base:
  ```python
  INSTALLED_APPS = [
      'apps.main.apps.MainConfig',
      'apps.veiculos.apps.VeiculosConfig',
      'apps.autenticacao.apps.AutenticacaoConfig',
      'widget_tweaks',
  ]
  ```

- Configurações de Mídia:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```

- Configurações de Arquivos Estáticos:
  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  ```

### Estrutura de URLs
- URLs Principais:
  - `/`: Homepage do sistema
  - `/admin/`: Interface administrativa
  - `/autenticacao/`: Rotas de autenticação
  - `/visitantes/`: Gestão de visitantes
  - `/veiculos/`: Controle de veículos

### Padrões de Desenvolvimento

#### Convenções de Código
- Estilo Python:
  - PEP 8 para código Python
  - Docstrings em todas as funções
  - Type hints em parâmetros críticos
  - Comentários em português

- Estilo Django:
  - Nomes de apps em português
  - Models com nomes no singular
  - Views com sufixo descritivo (_view)
  - URLs com nomes em português

#### Estrutura de Models
- Padrões Implementados:
  - Abstract base classes para campos comuns
  - Validators personalizados
  - Campos com verbose_name em português
  - Meta options padronizadas

#### Sistema de Templates
- Hierarquia de Templates:
  ```
  templates/
  ├── base.html
  ├── autenticacao/
  │   ├── login_sistema.html
  │   └── logout_sistema.html
  ├── main/
  │   ├── visitantes/
  │   │   ├── cadastro_visitantes.html
  │   │   ├── lista_visitantes.html
  │   │   └── historico_visitas.html
  │   └── recepcao/
  │       ├── status_visita.html
  │       └── home_sistema.html
  └── veiculos/
      ├── registro_entrada.html
      ├── registro_saida.html
      └── lista_veiculos.html
  ```

### Guia de Instalação

#### Requisitos do Sistema
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual (recomendado)
- Git para controle de versão

#### Passos de Instalação
1. Clonar o repositório:
   ```bash
   git clone <repositório>
   cd Projeto_SIGEPE
   ```

2. Criar e ativar ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar banco de dados:
   ```bash
   python manage.py migrate
   ```

5. Criar superusuário:
   ```bash
   python manage.py createsuperuser
   ```

6. Executar servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

### Boas Práticas de Segurança

#### Proteção de Dados
- Implementações:
  - Validação de CPF com máscara
  - Sanitização de inputs
  - Proteção contra CSRF
  - Controle de acesso por decorators

#### Autenticação
- Medidas Implementadas:
  - Sessões seguras
  - Timeout de inatividade
  - Bloqueio após tentativas falhas
  - Logs de acesso

#### Backup e Recuperação
- Estratégias:
  - Backup automático diário
  - Versionamento de migrations
  - Exportação de dados críticos
  - Procedimentos de restore

### Manutenção e Monitoramento

#### Logs do Sistema
- Implementação:
  - Logs estruturados por módulo
  - Rotação de arquivos de log
  - Níveis de severidade
  - Alertas automáticos

#### Performance
- Otimizações:
  - Cache de templates
  - Consultas otimizadas
  - Lazy loading de imagens
  - Compressão de assets

#### Monitoramento
- Métricas Implementadas:
  - Tempo de resposta
  - Uso de recursos
  - Erros e exceções
  - Acessos concorrentes

## Integrações e Padrões Específicos (12/03/2025)

### Integração entre Componentes
- Sistema de Visitantes e Veículos:
  - Vinculação de veículos a visitantes
  - Registro automático de entrada/saída
  - Histórico unificado de acessos
  - Dashboard integrado

### Padrões de Interface
- Elementos Consistentes:
  - Header com logo URUTAU
  - Navegação padronizada
  - Feedback visual uniforme
  - Modais de confirmação

### Fluxos de Dados
- Visitantes:
  ```
  Cadastro → Foto → Registro de Visita → Histórico
  ```
- Veículos:
  ```
  Registro → Vinculação → Controle → Saída
  ```

### Estrutura de Arquivos
- Organização Principal:
  ```
  Projeto_SIGEPE/
  ├── apps/
  │   ├── main/
  │   ├── veiculos/
  │   └── autenticacao/
  ├── static/
  │   ├── shared/
  │   ├── admin/
  │   └── img/
  ├── media/
  │   └── visitantes/
  ├── templates/
  │   ├── base.html
  │   └── [apps]/
  └── docs/
      └── README.md
  ```

### Convenções Específicas
- Nomenclatura de Arquivos:
  - Templates: `nome_funcionalidade.html`
  - Views: `nome_view.py`
  - URLs: `nome_urls.py`
  - Static: `nome_styles.css`, `nome_script.js`

- Padrões de Código:
  - Imports organizados por tipo
  - Docstrings descritivas em português
  - Comentários explicativos quando necessário
  - Type hints em funções críticas

### Fluxo de Desenvolvimento
1. Análise de Requisitos
2. Documentação de Mudanças
3. Implementação seguindo padrões
4. Testes e Validação
5. Revisão de Código
6. Deploy e Monitoramento

---
> Este documento será atualizado conforme novas melhorias forem implementadas no projeto.
> Última atualização: 12/03/2025