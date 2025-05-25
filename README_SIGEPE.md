# SIGEPE - Sistema de Gestão de Pessoas e Veículos

## Índice
- [1. Módulo Veículos](#1-módulo-veículos)
  - [Funcionalidades Gerais](#funcionalidades-gerais-veiculos)
  - [Páginas](#páginas-veiculos)
  - [Fluxos de Uso](#fluxos-veiculos)
  - [Endpoints Principais](#endpoints-veiculos)
- [2. Módulo Visitantes](#2-módulo-visitantes)
  - [Funcionalidades Gerais](#funcionalidades-gerais-visitantes)
  - [Páginas](#páginas-visitantes)
  - [Fluxos de Uso](#fluxos-visitantes)
  - [Endpoints Principais](#endpoints-visitantes)
- [3. Módulo Recepção](#3-módulo-recepção)
  - [Funcionalidades Gerais](#funcionalidades-gerais-recepcao)
  - [Páginas](#páginas-recepcao)
  - [Fluxos de Uso](#fluxos-recepcao)
  - [Endpoints Principais](#endpoints-recepcao)
- [4. Módulo Departamentos](#4-módulo-departamentos)
  - [Funcionalidades Gerais](#funcionalidades-gerais-departamentos)
  - [Páginas](#páginas-departamentos)
  - [Fluxos de Uso](#fluxos-departamentos)
  - [Endpoints Principais](#endpoints-departamentos)
- [5. Módulo Gabinetes](#5-módulo-gabinetes)
  - [Funcionalidades Gerais](#funcionalidades-gerais-gabinetes)
  - [Páginas](#páginas-gabinetes)
  - [Fluxos de Uso](#fluxos-gabinetes)
  - [Endpoints Principais](#endpoints-gabinetes)
- [6. Relatórios e Analytics](#6-relatórios-e-analytics)
- [7. Acessibilidade e UX](#7-acessibilidade-e-ux)
- [8. Administração e Segurança](#8-administração-e-segurança)
- [9. Observações Gerais](#9-observações-gerais)

---

## 1. Módulo Veículos

### <a name="funcionalidades-gerais-veiculos"></a>Funcionalidades Gerais
- Cadastro, edição e exclusão de veículos
- Validação automática de placas (ABC-1234 e Mercosul)
- Conversão automática para maiúsculas
- Cores padronizadas conforme DETRAN
- Tipos de veículos: Carro, Moto, Caminhonete, Caminhão, Ônibus, Outros
- Status do veículo: "Presente no Estacionamento" ou "Saída Realizada"
- Atualização automática do status
- Indicadores visuais e animações para status
- Busca e filtros por placa, modelo, cor, tipo e status
- Interface responsiva e moderna

### <a name="páginas-veiculos"></a>Páginas
- **Lista de Veículos**: Cards responsivos, busca em tempo real, separação entre presentes e histórico
- **Detalhes do Veículo**: Informações completas, histórico de entradas/saídas, botões de ação
- **Registro de Entrada/Saída**: Formulários rápidos, validação em tempo real
- **Relatórios**: Exportação em PDF, filtros avançados

### <a name="fluxos-veiculos"></a>Fluxos de Uso
1. **Cadastro de Veículo**: Usuário acessa `/veiculos/registro-entrada/`, preenche dados e salva.
2. **Saída de Veículo**: Usuário acessa `/veiculos/registro-saida/`, seleciona veículo e confirma saída.
3. **Consulta**: Usuário acessa `/veiculos/` para ver todos os veículos presentes e históricos.
4. **Detalhes**: Clica em uma placa na lista para acessar `/veiculos/detalhes/<id>/`.

### <a name="endpoints-veiculos"></a>Endpoints Principais
- `GET /veiculos/` — Lista de veículos
- `GET /veiculos/registro-entrada/` — Formulário de entrada
- `POST /veiculos/registro-entrada/` — Submissão de novo veículo
- `GET /veiculos/registro-saida/` — Formulário de saída
- `POST /veiculos/registro-saida/` — Confirmação de saída
- `GET /veiculos/lista-veiculos/` — Lista detalhada
- `GET /veiculos/historico/` — Histórico de veículos
- `GET /veiculos/detalhes/<id>/` — Detalhes do veículo

---

## 2. Módulo Visitantes

### <a name="funcionalidades-gerais-visitantes"></a>Funcionalidades Gerais
- Cadastro de visitantes com campos obrigatórios e opcionais
- Validação de CPF único
- Máscara e validação de telefone e data de nascimento
- Objetivo da visita padronizado (com campo "Outros")
- Upload de foto do visitante
- Busca por nome, nome social ou CPF
- Interface de visitas somente leitura (sem edição/exclusão)
- Criação automática de visita ao cadastrar visitante
- Status coloridos para visitas (em andamento/finalizada)
- Histórico de visitas por visitante

### <a name="páginas-visitantes"></a>Páginas
- **Cadastro de Visitante**: Formulário completo, feedback visual, máscara de campos
- **Lista de Visitantes**: Busca, links para detalhes, visualização de status
- **Detalhes do Visitante**: Foto, dados completos, histórico de visitas
- **Registro de Visitas**: Seleção de visitante, registro automático de entrada/saída
- **Histórico de Visitas**: Filtros por status, período, busca, exportação
- **Status das Visitas**: Painel de controle em tempo real, filtros por setor/localização

### <a name="fluxos-visitantes"></a>Fluxos de Uso
1. **Cadastro de Visitante**: Usuário acessa `/recepcao/cadastro-visitantes/`, preenche dados e salva.
2. **Registro de Visita**: Ao cadastrar visitante, visita é criada automaticamente.
3. **Consulta**: Usuário acessa `/recepcao/visitantes/` para ver todos os visitantes.
4. **Detalhes**: Clica em um nome para acessar `/recepcao/visitantes/<id>/`.
5. **Histórico**: Acessa `/recepcao/visitas/historico/` para consultar visitas passadas.

### <a name="endpoints-visitantes"></a>Endpoints Principais
- `GET /recepcao/visitantes/` — Lista de visitantes
- `GET /recepcao/cadastro-visitantes/` — Formulário de cadastro
- `POST /recepcao/cadastro-visitantes/` — Submissão de visitante
- `GET /recepcao/visitantes/<id>/` — Detalhes do visitante
- `GET /recepcao/visitas/historico/` — Histórico de visitas
- `GET /recepcao/visitas/status/` — Painel de status em tempo real

---

## 3. Módulo Recepção

### <a name="funcionalidades-gerais-recepcao"></a>Funcionalidades Gerais
- Painel de estatísticas (visitas hoje, em andamento, total, por mês)
- Cards informativos com gradiente e ícones
- Botão universal de "Voltar" em todas as páginas (exceto home)
- Ações rápidas para registro de visitantes e veículos
- Interface adaptada para recepcionistas (restrição de acesso)

### <a name="páginas-recepcao"></a>Páginas
- **Home Recepção**: Cards de estatísticas, ações rápidas
- **Cadastro de Visitantes**: Acesso rápido, formulário otimizado
- **Registro de Visitas**: Processo simplificado
- **Lista de Visitantes**: Consulta e navegação rápida
- **Histórico de Visitas**: Consulta detalhada, filtros
- **Status das Visitas**: Painel em tempo real

### <a name="fluxos-recepcao"></a>Fluxos de Uso
1. **Acesso ao Painel**: Usuário acessa `/recepcao/` para ver estatísticas e ações rápidas.
2. **Cadastro/Registro**: A partir do painel, pode acessar cadastro de visitantes ou registro de visitas.
3. **Consulta**: Acesso rápido a listas e históricos.

### <a name="endpoints-recepcao"></a>Endpoints Principais
- `GET /recepcao/` — Painel principal
- `GET /recepcao/lista-visitantes/` — Lista de visitantes
- `GET /recepcao/registro-visitas/` — Registro de visitas
- `GET /recepcao/historico-visitas/` — Histórico
- `GET /recepcao/status-visita/` — Status em tempo real

---

## 4. Módulo Departamentos

### <a name="funcionalidades-gerais-departamentos"></a>Funcionalidades Gerais
- Cadastro e visualização de departamentos/setores
- Cards informativos e responsivos
- Detalhamento de cada departamento
- Integração com registro de visitas

### <a name="páginas-departamentos"></a>Páginas
- **Home Departamentos**: Cards de cada departamento, estatísticas
- **Detalhes do Departamento**: Informações completas, histórico de visitas

### <a name="fluxos-departamentos"></a>Fluxos de Uso
1. **Consulta**: Usuário acessa `/recepcao/departamentos/` para ver todos os departamentos.
2. **Detalhes**: Clica em um card para acessar `/recepcao/departamentos/<id>/`.

### <a name="endpoints-departamentos"></a>Endpoints Principais
- `GET /recepcao/departamentos/` — Lista de departamentos
- `GET /recepcao/departamentos/<id>/` — Detalhes do departamento

---

## 5. Módulo Gabinetes

### <a name="funcionalidades-gerais-gabinetes"></a>Funcionalidades Gerais
- Cadastro e visualização de gabinetes/vereadores
- Cards informativos e responsivos
- Detalhamento de cada gabinete
- Integração com registro de visitas

### <a name="páginas-gabinetes"></a>Páginas
- **Home Gabinetes**: Cards de cada gabinete, estatísticas
- **Detalhes do Gabinete**: Informações completas, histórico de visitas

### <a name="fluxos-gabinetes"></a>Fluxos de Uso
1. **Consulta**: Usuário acessa `/recepcao/gabinetes/` para ver todos os gabinetes.
2. **Detalhes**: Clica em um card para acessar `/recepcao/gabinetes/<id>/`.

### <a name="endpoints-gabinetes"></a>Endpoints Principais
- `GET /recepcao/gabinetes/` — Lista de gabinetes
- `GET /recepcao/gabinetes/<id>/` — Detalhes do gabinete

---

## 6. Relatórios e Analytics
- Relatórios em PDF para veículos e visitas
- Filtros avançados por período, status, setor, visitante
- Exportação de dados
- Painéis de estatísticas em todas as áreas principais

---

## 7. Acessibilidade e UX
- Contraste adequado em todos os componentes
- Navegação por teclado e leitores de tela
- Botões e cards com feedback visual (hover, foco, toque)
- Layout responsivo para desktop, tablet e mobile
- Mensagens de erro claras e acessíveis

---

## 8. Administração e Segurança
- Interface administrativa completa do Django
- Controle de permissões por grupo (ex: Recepcionista)
- Validação de dados no cliente e servidor
- Proteção contra dados duplicados e inconsistentes
- Logs de alterações e auditoria

---

## 9. Observações Gerais
- Sistema modular, fácil de manter e evoluir
- Scripts de instalação automatizados para Windows
- Suporte a reconhecimento facial (opcional)
- Documentação e suporte disponíveis 