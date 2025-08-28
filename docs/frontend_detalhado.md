# Frontend Detalhado - Sistema SIGEPE

## Visão Geral

O Sistema SIGEPE (Sistema de Gestão de Pessoas e Veículos) possui uma interface web moderna e responsiva, construída com Bootstrap 5, Font Awesome e CSS customizado. O design segue princípios de UX/UI modernos com foco em acessibilidade e usabilidade.

---

## 🎨 Design System

### Cores e Variáveis CSS
```css
:root {
    --primary-color: #0D6EFD;
    --secondary-color: #34495e;
    --accent-color: #3498db;
    --success-color: #2ecc71;
    --warning-color: #f1c40f;
    --danger-color: #e74c3c;
    --light-color: #ecf0f1;
    --dark-color: #2c3e50;
}
```

### Gradientes Principais
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #238b8b 100%)`
- **Success Gradient**: `linear-gradient(135deg, #5cb85c, #28a745)`
- **Info Gradient**: `linear-gradient(135deg, #6dd5ed, #2193b0)`
- **Warning Gradient**: `linear-gradient(135deg, #f1c40f, #f39c12)`
- **Danger Gradient**: `linear-gradient(135deg, #e67e22, #e74c3c)`

### Tipografia
- **Fonte Principal**: Poppins (Google Fonts)
- **Pesos**: 300, 400, 500, 600, 700
- **Fallback**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif

---

## 🚗 Módulo Veículos

### Home do Módulo (`home_veiculos.html`)
**Características:**
- Dashboard com estatísticas em tempo real
- Cards informativos com gradientes coloridos
- Layout responsivo com Bootstrap Grid
- Ícones Font Awesome para melhor UX

**Componentes Principais:**
1. **Header do Dashboard**
   - Gradiente azul-verde
   - Título com ícone de estacionamento
   - Efeito de sobreposição com transparência

2. **Cards de Estatísticas**
   - Veículos no estacionamento (azul)
   - Veículos hoje (verde)
   - Veículos no mês (laranja)
   - Hover effects com transformação

3. **Cards de Ação**
   - Registro de entrada
   - Registro de saída
   - Lista de veículos
   - Histórico

### Registro de Entrada (`registro_entrada.html`)
**Funcionalidades:**
- Formulário de cadastro com validação
- Upload de foto do veículo
- Máscaras de input para placa
- Preview da foto em tempo real
- Responsivo para mobile

### Registro de Saída (`registro_saida.html`)
**Funcionalidades:**
- Busca por placa do veículo
- Confirmação de saída
- Cálculo automático de tempo
- Geração de comprovante

### Lista de Veículos (`lista_veiculos.html`)
**Características:**
- Tabela responsiva com Bootstrap
- Filtros de busca
- Paginação
- Status visual (presente/ausente)
- Ações rápidas por linha

---

## 👥 Módulo Recepção

### Home da Recepção (`home_recepcao.html`)
**Dashboard Principal:**
- **Widget de Tempo**: Relógio em tempo real
- **Cards de Estatísticas**:
  - Visitantes hoje
  - Visitas em andamento
  - Total de visitas
  - Departamentos ativos

**Seções Principais:**
1. **Ações Rápidas**
   - Cadastro de visitante
   - Registro de visita
   - Totem de autoatendimento

2. **Visitas em Andamento**
   - Lista em tempo real
   - Status visual
   - Ações de finalização

3. **Departamentos Ativos**
   - Cards informativos
   - Horários de funcionamento
   - Status de disponibilidade

### Cadastro de Visitantes (`cadastro_visitantes.html`)
**Formulário Completo:**
- Validação de CPF em tempo real
- Upload de foto com preview
- Máscaras de input
- Validação de dados
- Responsivo para mobile

### Registro de Visitas (`registro_visitas.html`)
**Interface Avançada:**
- Busca inteligente de visitantes
- Seleção de departamento/gabinete
- Controle de horários
- Geração de etiquetas
- Histórico de visitas

---

## 🏢 Módulo Departamentos

### Home de Departamentos (`home_departamentos.html`)
**Layout de Cards:**
- Cards informativos por departamento
- Foto do responsável
- Horário de funcionamento
- Status de disponibilidade
- Contador de visitas

### Detalhes do Departamento (`detalhes_departamento.html`)
**Informações Detalhadas:**
- Foto do setor
- Informações do responsável
- Horários de funcionamento
- Histórico de visitas
- Ações administrativas

---

## 🏛️ Módulo Gabinetes

### Home de Gabinetes (`home_gabinetes.html`)
**Interface Similar aos Departamentos:**
- Cards informativos
- Foto do gabinete
- Informações do responsável
- Status de disponibilidade

### Detalhes do Gabinete (`detalhes_gabinete.html`)
**Funcionalidades:**
- Informações completas
- Histórico de visitas
- Edição de dados
- Controle de acesso

---

## 📊 Módulo Relatórios

### Dashboard de Relatórios (`dashboard.html`)
**Gráficos e Estatísticas:**
- Gráficos interativos (Chart.js)
- Filtros por período
- Exportação em PDF
- Métricas em tempo real

**Tipos de Relatórios:**
- Relatório de visitas
- Relatório de veículos
- Relatório de departamentos
- Relatório de gabinetes

---

## 🤖 Módulo Totem (Autoatendimento)

### Base do Totem (`base_totem.html`)
**Características Especiais:**
- Interface otimizada para touchscreen
- Botões grandes e acessíveis
- Navegação simplificada
- Sem header/footer tradicional

### Tela de Boas-vindas (`totem_welcome.html`)
**Interface de Entrada:**
- Logo institucional
- Mensagem de boas-vindas
- Botão de início grande
- Design minimalista

### Identificação (`totem_identificacao.html`)
**Reconhecimento Facial:**
- Interface de câmera
- Instruções visuais
- Feedback em tempo real
- Validação de identidade

### Seleção de Destino (`totem_destino.html`)
**Navegação por Destino:**
- Lista de departamentos e lista gabinetes em grade com foto aredondada
- Cards grandes para touch
- Busca por nome
- Confirmação visual

### Comprovante (`totem_comprovante.html`)
**Geração de Comprovante:**
- Layout de impressão
- QR Code
- Informações da visita
- Opção de impressão térmica

---

## 🔐 Módulo Autenticação

### Login do Sistema (`login_sistema.html`)
**Interface de Login:**
- Formulário centralizado
- Validação em tempo real
- Mensagens de erro
- Design responsivo

### Perfil do Usuário (`perfil_usuario.html`)
**Gerenciamento de Conta:**
- Informações pessoais
- Alteração de senha
- Preferências
- Histórico de atividades

---

## 🎯 Componentes Reutilizáveis

### Cards de Estatísticas
```css
.stat-card {
    color: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    height: 180px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Botões de Ação
```css
.btn {
    border-radius: 5px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}
```

### Tabelas Responsivas
- Bootstrap Table
- Paginação
- Filtros
- Ordenação
- Ações por linha

---

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Adaptações Mobile
- Cards empilhados
- Botões maiores
- Navegação simplificada
- Formulários otimizados

---

## ♿ Acessibilidade

### Recursos Implementados
- Navegação por teclado
- Contraste adequado
- Textos alternativos
- Estrutura semântica
- Foco visual

### Melhorias de UX
- Feedback visual
- Loading states
- Mensagens de erro claras
- Confirmações de ação

---

## 🎨 Animações e Transições

### Hover Effects
```css
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,.15);
}
```

### Transições Suaves
```css
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Loading Animations
- Spinners personalizados
- Skeleton loading
- Progress bars

---

## 🔧 Tecnologias Utilizadas

### Frontend
- **Bootstrap 5**: Framework CSS
- **Font Awesome 6**: Ícones
- **Google Fonts**: Tipografia
- **Chart.js**: Gráficos
- **jQuery**: Manipulação DOM

### Recursos
- **CSS Grid/Flexbox**: Layout
- **CSS Variables**: Manutenibilidade
- **Media Queries**: Responsividade
- **JavaScript ES6+**: Interatividade

---

## 📋 Checklist de Qualidade

### Design
- [x] Interface moderna e limpa
- [x] Consistência visual
- [x] Hierarquia clara
- [x] Cores acessíveis

### Usabilidade
- [x] Navegação intuitiva
- [x] Feedback visual
- [x] Formulários validados
- [x] Mensagens claras

### Performance
- [x] Carregamento otimizado
- [x] Imagens comprimidas
- [x] CSS minificado
- [x] Lazy loading

### Acessibilidade
- [x] Navegação por teclado
- [x] Contraste adequado
- [x] Textos alternativos
- [x] Estrutura semântica

---

## 🚀 Próximas Melhorias

### Planejadas
- Dark mode
- PWA (Progressive Web App)
- Notificações push
- Temas customizáveis

### Otimizações
- Lazy loading de imagens
- Code splitting
- Service workers
- Cache inteligente

---

*Documentação criada para o Sistema SIGEPE - Versão 1.0*
