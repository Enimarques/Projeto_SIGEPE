# Sistema de Permissões Melhorado - SIGEPE

## Visão Geral

O sistema SIGEPE foi aprimorado com um sistema de permissões mais granular e personalizado, onde cada tipo de usuário tem acesso específico apenas aos módulos e informações relevantes para sua função.

---

## Tipos de Usuários e Permissões

### 1. **Administradores**
- **Acesso**: Total ao sistema
- **Módulos**: Todos os módulos disponíveis
- **Home**: Dashboard completo com estatísticas gerais
- **Relatórios**: Dados de todo o sistema
- **Funcionalidades**: Gerenciamento de usuários, configurações do sistema

### 2. **Assessores**
- **Acesso**: Restrito ao seu gabinete/departamento específico
- **Módulos**: 
  - Seu gabinete/departamento
  - Relatórios específicos do seu setor
- **Home**: Dashboard personalizado com estatísticas do seu setor
- **Relatórios**: Filtrados automaticamente pelo seu gabinete/departamento
- **Restrições**: Não podem acessar outros gabinetes ou módulos de veículos

### 3. **Agente de Guarita**
- **Acesso**: Apenas ao módulo de veículos
- **Módulos**: 
  - Controle de veículos
  - Relatórios de veículos
- **Home**: Dashboard focado em estatísticas de veículos
- **Restrições**: Não podem acessar módulos de recepção ou gabinetes

### 4. **Recepcionista**
- **Acesso**: Módulos de recepção e visualização de gabinetes
- **Módulos**:
  - Recepção de visitantes
  - Visualização de gabinetes (sem edição)
  - Modo TOTEM
- **Home**: Dashboard focado em visitantes e recepção
- **Restrições**: Não podem gerenciar veículos ou acessar relatórios administrativos

---

## Implementação Técnica

### 1. **Sistema de Verificação de Permissões**

#### **AuthenticationService** (`apps/autenticacao/services/auth_service.py`)
```python
class AuthenticationService:
    @staticmethod
    def is_admin(user):
        return user.is_superuser or user.groups.filter(name='Administradores').exists()
    
    @staticmethod
    def is_assessor(user):
        try:
            return hasattr(user, 'assessor') and user.assessor.ativo
        except:
            return False
    
    @staticmethod
    def is_recepcionista(user):
        return user.groups.filter(name='Recepcionista').exists()
```

#### **Decorators de Controle de Acesso** (`apps/autenticacao/decorators.py`)
```python
@assessor_own_gabinete_only
def detalhes_gabinete(request, pk):
    # Restringe assessores apenas ao seu próprio gabinete
    pass

@block_assessor
def home_gabinetes(request):
    # Bloqueia assessores de acessar a lista geral de gabinetes
    pass
```

### 2. **Home Personalizada por Tipo de Usuário**

#### **View Principal** (`apps/main/views.py`)
```python
def home_sistema(request):
    user = request.user
    is_assessor = AuthenticationService.is_assessor(user)
    is_guarita = 'Agente_Guarita' in user.groups.all()
    
    if is_assessor:
        # Dados específicos do gabinete do assessor
        context['visitas_hoje_gabinete'] = Visita.objects.filter(
            setor=user.assessor.departamento,
            data_entrada__date=hoje
        ).count()
    elif is_guarita:
        # Dados específicos de veículos
        context['veiculos_entraram_hoje'] = Veiculo.objects.filter(
            historico__data_entrada__date=hoje
        ).distinct().count()
```

### 3. **Relatórios Filtrados por Gabinete**

#### **Views de Relatórios** (`apps/relatorios/views.py`)
```python
@login_required
def api_cards(request):
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        departamento = request.user.assessor.departamento
    
    # Filtrar visitas por departamento se for assessor
    visitas_queryset = Visita.objects.all()
    if departamento:
        visitas_queryset = visitas_queryset.filter(setor=departamento)
```

---

## Interface do Usuário

### 1. **Home Personalizada**

#### **Assessores**
- **Mensagem de boas-vindas**: "Bem-vindo, [Nome]! Você está logado como assessor do [Gabinete/Departamento]"
- **Cards de estatísticas**: Visitas em andamento, visitas hoje, total de visitas do seu setor
- **Módulos disponíveis**: 
  - "Meu Gabinete/Departamento"
  - "Relatórios do Gabinete/Departamento"

#### **Agente de Guarita**
- **Mensagem de boas-vindas**: "Bem-vindo, [Nome]! Você está logado como Agente de Guarita"
- **Cards de estatísticas**: Veículos no estacionamento, veículos cadastrados, entrada/saída hoje
- **Módulos disponíveis**:
  - "Módulo de Veículos"
  - "Relatórios de Veículos"

#### **Recepcionista**
- **Mensagem de boas-vindas**: "Bem-vindo, [Nome]! Você está logado como Recepcionista"
- **Cards de estatísticas**: Visitas em andamento, visitantes hoje, total de visitantes
- **Módulos disponíveis**:
  - "Módulo de Recepção"
  - "Módulo de Gabinetes" (visualização)
  - "Modo TOTEM"

### 2. **Relatórios Específicos**

#### **Para Assessores**
- **Título**: "Relatórios do Gabinete [Nome]" ou "Relatórios do Departamento [Nome]"
- **Informações do setor**: Localização, horário de funcionamento
- **Dados filtrados**: Apenas visitas do seu gabinete/departamento
- **Exportação**: Arquivos nomeados com o nome do setor

---

## Segurança e Controle de Acesso

### 1. **Decorators de Segurança**

#### **@assessor_own_gabinete_only**
- Restringe assessores apenas ao seu próprio gabinete/departamento
- Redireciona automaticamente se tentar acessar outro setor
- Mensagem: "Você só pode acessar informações do seu próprio gabinete/departamento"

#### **@block_assessor**
- Bloqueia assessores de acessar áreas administrativas
- Redireciona para o gabinete do assessor
- Mensagem: "Assessores não têm acesso a esta área do sistema"

### 2. **Filtros Automáticos**

#### **Relatórios**
- Assessores veem apenas dados do seu setor
- Administradores veem dados de todo o sistema
- Filtros aplicados automaticamente sem intervenção do usuário

#### **Listas e Consultas**
- Assessores só veem visitas do seu gabinete/departamento
- Agentes de guarita só veem dados de veículos
- Recepcionistas veem dados de recepção e visualização de gabinetes

---

## Benefícios do Sistema

### 1. **Segurança**
- Controle granular de acesso por tipo de usuário
- Isolamento de dados entre setores
- Prevenção de acesso não autorizado

### 2. **Usabilidade**
- Interface personalizada para cada função
- Informações relevantes em destaque
- Navegação simplificada

### 3. **Manutenibilidade**
- Código centralizado para verificação de permissões
- Decorators reutilizáveis
- Fácil adição de novos tipos de usuário

### 4. **Performance**
- Filtros aplicados no nível do banco de dados
- Redução de dados desnecessários carregados
- Consultas otimizadas por tipo de usuário

---

## Como Configurar Novos Usuários

### 1. **Criar Assessor**
```bash
# 1. Criar usuário no Django Admin
# 2. Cadastrar assessor em Recepção > Assessores
# 3. Vincular usuário ao assessor no campo "Usuário"
# 4. Definir departamento/gabinete
# 5. Marcar como "Ativo"
```

### 2. **Criar Agente de Guarita**
```bash
# 1. Criar usuário no Django Admin
# 2. Adicionar ao grupo "Agente_Guarita"
# 3. Configurar permissões específicas se necessário
```

### 3. **Criar Recepcionista**
```bash
# 1. Criar usuário no Django Admin
# 2. Adicionar ao grupo "Recepcionista"
# 3. Configurar permissões específicas se necessário
```

---

## Troubleshooting

### 1. **Assessor não vê seu gabinete**
- Verificar se o campo "Usuário" está preenchido no cadastro do assessor
- Confirmar se o assessor está marcado como "Ativo"
- Verificar se o departamento está corretamente vinculado

### 2. **Usuário vê módulos indevidos**
- Verificar grupos do usuário no Django Admin
- Confirmar se não há múltiplos vínculos (ex: assessor + outro grupo)
- Limpar cache do navegador se necessário

### 3. **Relatórios não filtrados**
- Verificar se o assessor tem departamento vinculado
- Confirmar se as views estão usando os decorators corretos
- Verificar logs do sistema para erros

---

## Próximos Passos

### 1. **Melhorias Futuras**
- Dashboard mais detalhado para cada tipo de usuário
- Notificações personalizadas por setor
- Relatórios em tempo real
- Auditoria de acesso por usuário

### 2. **Monitoramento**
- Logs de acesso por tipo de usuário
- Métricas de uso por módulo
- Alertas de tentativas de acesso não autorizado

---

## Conclusão

O sistema de permissões melhorado garante que cada usuário tenha acesso apenas às informações relevantes para sua função, melhorando a segurança, usabilidade e performance do sistema SIGEPE. A implementação é escalável e permite fácil adição de novos tipos de usuário e permissões conforme necessário.

