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
16. [Instalação](#instalação)

obs- comando para não bagunçar!
certo! A partir de agora NÃO MEXA MAIS EM NENHUM OUTRO APP A NAO SER O APP DE RECEPCAO! seremos 3 desenvolvedores e nao queremos mexer no app dos outros! crie memoria.

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

## Melhorias Recentes

### Aprimoramentos nos Templates (12/03/2025)

#### Template de Lista de Veículos (lista_veiculos.html)
- Adicionados links clicáveis nas placas dos veículos
- Substituído o modal por uma página dedicada de detalhes
- Melhorada a estilização e organização dos botões
- Adicionados links adequados para a página de detalhes do veículo
- Implementada busca em tempo real de veículos
- Separação clara entre veículos presentes e histórico de saídas

#### Template de Detalhes do Veículo (detalhes_veiculo.html)
- Corrigidos erros de lint no CSS
- Adicionadas classes de cores predefinidas para os veículos
- Melhorado o design dos cartões e tabelas
- Aprimorados os efeitos de hover nos botões
- Adicionada navegação adequada de volta para a lista
- Layout responsivo e adaptável

#### Template de Lista de Visitantes (lista_visitantes.html)
- Adicionados links clicáveis nos nomes dos visitantes
- Substituído o modal por uma página dedicada de detalhes
- Melhorada a estilização e organização dos botões
- Adicionados links adequados para a página de detalhes do visitante
- Interface mais limpa e organizada
- Melhor visualização do status das visitas

#### Novo Template de Detalhes do Visitante (detalhes_visitante.html)
- Exibição detalhada das informações do visitante
- Inclusão de foto do visitante com ícone de fallback
- Histórico de visitas com links para os veículos correspondentes
- Estilização consistente com a página de detalhes do veículo
- Adicionada navegação adequada de volta para a lista
- Informações organizadas em seções lógicas

### Padrões de Design e Cores

#### Esquema de Cores do Sistema
- Primária: #007bff (Azul)
- Secundária: #6c757d (Cinza)
- Sucesso: #28a745 (Verde)
- Perigo: #dc3545 (Vermelho)
- Aviso: #ffc107 (Amarelo)
- Info: #17a2b8 (Azul claro)
- Claro: #f8f9fa (Branco)
- Escuro: #343a40 (Preto)

#### Tipografia
- Fonte principal: Roboto
- Tamanhos:
  - Títulos: 24px
  - Subtítulos: 18px
  - Texto normal: 16px
  - Texto pequeno: 14px
- Pesos:
  - Regular: 400
  - Medium: 500
  - Bold: 700

#### Espaçamento
- Padding padrão: 1rem
- Margem padrão: 1rem
- Gutter do grid: 30px
- Espaçamento entre elementos: 0.5rem

#### Componentes
- Botões:
  - Padding: 0.5rem 1rem
  - Border-radius: 4px
  - Transição: 0.3s
- Cards:
  - Border-radius: 8px
  - Sombra: 0 2px 4px rgba(0,0,0,0.1)
  - Padding: 1.5rem
- Tabelas:
  - Cabeçalho: fundo cinza claro
  - Linhas alternadas
  - Hover em linhas
  - Padding: 0.75rem

### Responsividade
- Breakpoints:
  - Mobile: < 576px
  - Tablet: 576px - 768px
  - Desktop: > 768px
- Adaptações:
  - Menu colapsável em mobile
  - Cards em grid responsivo
  - Tabelas com scroll horizontal
  - Fontes ajustáveis

### Acessibilidade
- Contraste adequado
- Textos redimensionáveis
- Navegação por teclado
- Labels semânticos
- ARIA labels quando necessário
- Mensagens de erro claras

### Performance
- Lazy loading de imagens
- Minificação de assets
- Cache de recursos estáticos
- Otimização de queries
- Paginação de resultados
- Debounce em buscas

## Instalação

### Requisitos do Sistema
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Virtualenv (recomendado)

### Passos para Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/SIGEPE.git
cd SIGEPE
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

### Configurações Adicionais

#### Configuração do Banco de Dados
- Por padrão, o sistema usa SQLite
- Para PostgreSQL:
  - Instale o psycopg2
  - Atualize as configurações no settings.py

#### Configuração de Email
- Configure o servidor SMTP no .env
- Teste o envio de emails:
```bash
python manage.py test_email
```

#### Configuração de Armazenamento
- Por padrão, arquivos são salvos localmente
- Para AWS S3:
  - Instale django-storages
  - Configure as credenciais no .env

### Solução de Problemas

#### Erros Comuns
1. Erro de migração:
```bash
python manage.py migrate --fake-initial
```

2. Erro de dependências:
```bash
pip install -r requirements.txt --upgrade
```

3. Erro de permissão:
```bash
chmod +x manage.py
```

#### Logs
- Logs são salvos em logs/
- Nível de log configurável no settings.py
- Rotação de logs automática

### Manutenção

#### Backup
- Backup automático diário
- Retenção de 7 dias
- Compactação automática

#### Atualização
```bash
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

#### Limpeza
```bash
python manage.py cleanup_old_data
python manage.py cleanup_media
```

## Suporte

### Canais de Suporte
- Email: suporte@sigepe.com
- Telefone: (11) 1234-5678
- Chat: https://chat.sigepe.com

### Documentação
- Manual do usuário: /docs/manual.pdf
- API: /docs/api/
- Guias: /docs/guides/

### Treinamento
- Vídeos tutoriais
- Workshops mensais
- Material de apoio

## Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
