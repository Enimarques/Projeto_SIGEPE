# Documentação do Modo Totem - URUTAU

Sistema completo de reconhecimento facial e gestão autônoma de visitas para câmaras municipais.

## 📚 Índice da Documentação

### **Documentos Principais:**
1. **[01_visao_geral.md](01_visao_geral.md)** - Visão geral do sistema e funcionalidades
2. **[02_fluxo_usuario.md](02_fluxo_usuario.md)** - Jornada do usuário e wireframes
3. **[03_arquitetura.md](03_arquitetura.md)** - Arquitetura técnica e componentes
4. **[04_reconhecimento_facial.md](04_reconhecimento_facial.md)** - Detalhes da IA e reconhecimento
5. **[05_configuracao_e_dependencias.md](05_configuracao_e_dependencias.md)** - Setup e dependências
6. **[06_funcionalidade_finalizar_visita.md](06_funcionalidade_finalizar_visita.md)** - Nova funcionalidade de finalização

### **Documentação Adicional:**
- **[totem_finalize_search_documentacao.md](../totem_finalize_search_documentacao.md)** - Documentação técnica detalhada da página de finalizar visita

---

## 🚀 Novidades Implementadas

### **✨ Últimas Atualizações (2024):**

#### **🎯 Sistema Dual de Finalização**
- **Reconhecimento Facial**: MediaPipe para detecção automática
- **Busca Manual**: Por nome, CPF ou nome social
- **Finalização Automática**: Encerra todas as visitas ativas

#### **🎨 Interface Moderna**
- **Design Consistente**: Gradientes e tipografia Poppins
- **Feedback Visual**: Overlays coloridos e mensagens dinâmicas
- **Responsividade**: Adaptação para diferentes resoluções

#### **🤖 Tecnologia Avançada**
- **MediaPipe Tasks Vision**: Substitui face-api.js
- **ES6+ Modules**: JavaScript moderno via CDN
- **Performance Otimizada**: RequestAnimationFrame e debounce

#### **🔧 Melhorias Técnicas**
- **APIs REST Robustas**: Endpoints especializados
- **Tratamento de Erros**: Validações e fallbacks
- **Logging Detalhado**: Auditoria completa de ações

---

## 📱 Páginas do Sistema

### **🏠 Página Inicial - Welcome**
- **URL**: `/recepcao/totem/welcome/`
- **Função**: Ponto de entrada do sistema
- **Características**: Design elegante, navegação principal

### **🎥 Reconhecimento Facial - Identificação**
- **URL**: `/recepcao/totem/`
- **Função**: Identificação de visitantes por IA
- **Características**: MediaPipe, overlays visuais, feedback em tempo real

### **🎯 Seleção de Destino**
- **URL**: `/recepcao/totem/destino/`
- **Função**: Escolha do setor/gabinete de destino
- **Características**: Interface touch-friendly, validação

### **🏁 Finalizar Visita**
- **URL**: `/recepcao/totem/finalize_search/`
- **Função**: Encerramento autônomo de visitas
- **Características**: Sistema dual (facial + manual)

### **📄 Comprovante**
- **URL**: `/recepcao/totem/comprovante/<id>/`
- **Função**: Exibição e impressão de comprovante
- **Características**: Impressão automática, etiqueta 60x40mm

---

## 🔧 Configuração Rápida

### **1. Dependências Backend:**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### **2. Verificação Frontend:**
- **Navegador**: Chrome 90+ ou Edge 90+
- **Câmera**: 720p mínimo, 1080p recomendado
- **Conexão**: Internet para CDNs (MediaPipe, Bootstrap, etc.)

### **3. URLs de Teste:**
- http://127.0.0.1:8000/recepcao/totem/welcome/
- http://127.0.0.1:8000/recepcao/totem/
- http://127.0.0.1:8000/recepcao/totem/finalize_search/

---

## 🎯 Principais Funcionalidades

### **Para Visitantes:**
- ✅ **Identificação Automática**: Reconhecimento facial sem contato
- ✅ **Seleção de Destino**: Interface intuitiva para escolher setor
- ✅ **Finalização Autônoma**: Encerrar visita sem ir à recepção
- ✅ **Comprovante Digital**: Impressão automática de etiqueta

### **Para Recepção:**
- ✅ **Redução de Carga**: Menos demanda para atendimento presencial
- ✅ **Registros Precisos**: Horários automáticos de entrada/saída
- ✅ **Auditoria Completa**: Logs detalhados de todas as ações
- ✅ **Gestão Eficiente**: Painel administrativo integrado

### **Para Administração:**
- ✅ **Relatórios Avançados**: Métricas de uso e performance
- ✅ **Segurança Robusta**: Validações e proteções CSRF
- ✅ **Escalabilidade**: Preparado para grandes volumes
- ✅ **Manutenibilidade**: Código modular e documentado

---

## 🔍 Troubleshooting

### **Problemas Comuns:**

#### **🎥 Câmera não funciona:**
- Verificar permissões do navegador
- Testar com diferentes dispositivos USB
- Atualizar drivers da câmera

#### **🤖 MediaPipe não carrega:**
- Verificar conexão com internet
- Testar em navegador atualizado
- Verificar console para erros JavaScript

#### **🐍 face_recognition falha:**
- Instalar/recompilar dlib
- Verificar versão do Python
- Testar com imagens menores

#### **📱 Interface quebrada:**
- Verificar CDNs (Bootstrap, Font Awesome)
- Limpar cache do navegador
- Testar em modo privado/incógnito

---

## 📊 Arquitetura Atual

```
Frontend (Browser)
├── MediaPipe Tasks Vision (CDN)
├── Bootstrap 5 + Font Awesome (CDN)
├── JavaScript ES6+ Modules
└── Canvas Overlay + Video Stream

Backend (Django)
├── face_recognition + dlib
├── APIs REST especializadas
├── Models otimizados
└── Logging e auditoria

Hardware
├── Câmera HD (720p+)
├── Impressora térmica (60x40mm)
├── Totem touch screen
└── Conexão estável (CDNs)
```

---

## 📈 Próximos Passos

### **Melhorias Futuras:**
- 🔮 **IA Avançada**: Modelos mais precisos
- 📊 **Analytics**: Dashboard em tempo real
- 🔐 **Biometria Adicional**: Impressão digital, íris
- 🌐 **PWA**: App offline-first
- 🎨 **Temas**: Personalização visual
- 📱 **Mobile**: Versão para smartphones

---

## 👥 Equipe e Suporte

### **Desenvolvido por:**
- **Sistema URUTAU** - Câmara Municipal de Parauapebas
- **Departamento de Tecnologia da Informação**

### **Tecnologias Utilizadas:**
- **Backend**: Django, Python, face_recognition
- **Frontend**: MediaPipe, Bootstrap 5, ES6+
- **IA**: Google MediaPipe, dlib
- **UI/UX**: Design System moderno e responsivo

---

**📅 Última Atualização:** Dezembro 2024  
**🔄 Versão da Documentação:** 2.0  
**📋 Status:** Produção Ativa 