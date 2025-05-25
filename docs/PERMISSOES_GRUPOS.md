# Permissões de Grupos do SIGEPE

## Visão Geral
Este documento descreve toda a lógica de permissões, ajustes de frontend e backend, e as principais decisões para garantir que cada grupo de usuário tenha acesso apenas ao que lhe é permitido no sistema SIGEPE.

---

## Grupos e Permissões

### Administradores
- Acesso total a todos os módulos do sistema
- Gerenciamento de usuários (criar, editar, excluir)
- Gerenciamento de visitantes
- Gerenciamento de veículos
- Gerenciamento de setores e gabinetes
- Acesso a todos os relatórios
- Acesso ao painel administrativo do Django

### Assessores
- Acesso restrito ao seu próprio gabinete/departamento
- Visualização e edição de informações do seu setor
- Visualização de visitantes e visitas relacionadas ao seu setor
- Não pode gerenciar veículos
- Não pode acessar o painel administrativo do Django
- Não pode criar ou excluir usuários

### Agente_Guarita
- Acesso apenas ao módulo de veículos
- Registrar entrada e saída de veículos
- Visualizar e gerar relatórios de movimentação de veículos
- Não pode acessar informações de visitantes, setores ou gabinetes
- Não pode criar, editar ou excluir usuários
- Não pode acessar o painel administrativo do Django

---

## Lógica de Backend

- **Decorators**: Foram criados decorators específicos para restringir o acesso às views de veículos apenas para administradores e agentes de guarita (`agente_guarita_or_admin_required`).
- **Views**: A view `home_sistema` foi ajustada para identificar o grupo do usuário e exibir apenas os cards e módulos permitidos. Para o grupo Agente_Guarita, só aparecem os cards e o módulo de veículos.
- **Permissões de acesso**: Todas as views sensíveis de veículos usam o decorator para garantir que apenas usuários autorizados possam acessar.

---

## Lógica de Frontend

- **Menu dinâmico**: O template `base.html` foi ajustado para exibir apenas os menus permitidos para cada grupo, usando um filtro customizado de grupos (`grupos_tags`).
- **Dashboard**: O template `main/home_sistema.html` mostra apenas os cards e módulos de veículos para o grupo Agente_Guarita, escondendo os demais módulos (Gabinetes, Visitantes, Recepção).
- **Filtro customizado**: Criado em `apps/autenticacao/templatetags/grupos_tags.py` para facilitar a verificação dos grupos do usuário nos templates.

---

## Dicas de Manutenção

- Sempre que criar um novo grupo, adicione as permissões e lógica correspondente nos decorators e nos templates.
- Para adicionar novos módulos, siga o padrão de checagem de grupo tanto no backend (views) quanto no frontend (templates).
- Se o menu ou cards não aparecerem corretamente, verifique se o filtro customizado está sendo carregado e se o grupo do usuário está correto.
- Reinicie o servidor Django sempre que criar ou alterar filtros customizados.

---

## Resumo da Implementação

1. **Criação dos grupos**: Administradores, Assessores, Agente_Guarita (via admin ou script).
2. **Ajuste do backend**: Decorators e views protegendo o acesso.
3. **Ajuste do frontend**: Menus e cards condicionais por grupo.
4. **Filtro customizado**: Para facilitar a lógica nos templates.
5. **Testes**: Sempre testar com usuários de cada grupo para garantir a experiência correta.

---

Se precisar expandir as permissões ou adicionar novos grupos, siga este padrão para garantir segurança e clareza no sistema. 