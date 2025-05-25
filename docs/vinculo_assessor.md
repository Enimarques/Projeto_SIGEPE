# Documentação: Lógica e Funcionamento do Vínculo de Assessor no SIGEPE

## 1. Visão Geral
O sistema SIGEPE possui controle de acesso baseado em grupos e vínculos de usuário, especialmente para o perfil de Assessor. O vínculo correto garante que o usuário veja apenas os módulos permitidos e tenha acesso restrito conforme sua função.

---

## 2. Como funciona o vínculo de Assessor

### 2.1. Modelo Assessor
O modelo `Assessor` está localizado em `apps/recepcao/models.py` e possui um campo `usuario` (ForeignKey para o modelo User do Django). Esse campo é o responsável por vincular o Assessor a um usuário do sistema.

```
[Usuário criado no Admin]
      |
      v
[Assessor cadastrado em Recepção > Assessores]
      |
      v
[No cadastro do Assessor, campo "Usuário" é preenchido com o usuário desejado]
      |
      v
[Assessor salvo com campo "ativo" = True]
      |
      v
[Usuário faz login]
      |
      v
[Sistema verifica: existe Assessor ativo vinculado a este usuário?]
      |         \
      |          \
      v           v
[Sim]         [Não]
  |             |
  v             v
[Exibe apenas   [Exibe módulos conforme outros vínculos/permissões]
 Gabinetes]
```

### 2.2. Passo a Passo Detalhado

1. **Crie o usuário normalmente no Django Admin**
   - Menu: `Admin > Usuários`
   - Preencha nome, e-mail, senha, etc.
2. **Cadastre o Assessor**
   - Menu: `Recepção > Assessores`
   - Clique em "Adicionar Assessor"
   - Preencha os dados do assessor (nome, gabinete, etc.)
   - **No campo "Usuário" selecione o usuário criado no passo 1**
   - Marque "Ativo" se o assessor deve ter acesso
   - Salve
3. **Login e Teste**
   - Faça login com o usuário vinculado
   - O sistema deve exibir apenas o card de Gabinetes na home
   - Os módulos de Veículos e Recepção não aparecem
- **Dica:** Sempre vincule o usuário correto ao Assessor no admin. Sem esse vínculo, o sistema não reconhecerá o 
perfil de Assessor, mesmo que o usuário esteja no grupo "Assessores".


### 2.3. Exemplo Visual (Admin)

- ![Exemplo de cadastro de Assessor no admin](exemplo_admin_assessor.png)
- Campo "Usuário" é obrigatório
- Campo "Ativo" define se o vínculo está válido

### 2.4. Lógica de Backend

- O método `AuthenticationService.is_assessor(user)` verifica se existe um Assessor ativo vinculado ao usuário logado:

```python
class AuthenticationService:
    @staticmethod
    def is_assessor(user):
        return Assessor.objects.filter(usuario=user, ativo=True).exists()
```
- O sistema verifica se existe um Assessor ativo vinculado ao usuário logado.

- O contexto `is_assessor` é passado para o template:

```python
def home_sistema(request):
    user = request.user
    is_assessor = AuthenticationService.is_assessor(user)
    context['is_assessor'] = is_assessor
    ...
```
- O contexto `is_assessor` é passado para o template para controlar o que será exibido.

### 2.5. Controle de Exibição no Frontend
No template da home (`templates/main/home_sistema.html`), a exibição dos cards é controlada por `is_assessor`:

```django
{% if is_assessor %}
    <!-- Exibe apenas o card de Gabinetes para Assessores -->
{% endif %}
```
- O card do Módulo de Recepção não é exibido para Assessores.
- O card de Veículos também não aparece para Assessores.

### 2.6. Restrições de Permissão
- O grupo "Assessores" pode ser usado para permissões adicionais, mas o vínculo real é feito pelo campo `usuario` no modelo Assessor.
- O sistema pode usar decorators ou funções utilitárias para restringir views e ações conforme o perfil.

- **O usuário não vê o card de Gabinetes:**
  - Verifique se o campo "Usuário" está preenchido corretamente no cadastro do Assessor.
  - Confirme se o campo "Ativo" está marcado.
  - O usuário está no grupo "Assessores"? (opcional, mas não substitui o vínculo no modelo)
- **O usuário vê módulos indevidos:**
  - Pode haver mais de um vínculo (ex: está em outro grupo ou tem outro perfil ativo).
  - Verifique se o usuário não está vinculado a outro perfil (ex: Recepcionista).
- **Erro de permissão:**
  - Revise as permissões do grupo e o vínculo no modelo Assessor.

## 3. Passo a Passo para Vincular um Assessor
1. Cadastre o usuário normalmente no Django Admin.
2. Cadastre ou edite o Assessor em "Recepção > Assessores".
3. No campo "Usuário", selecione o usuário desejado.
4. Salve. Pronto! O vínculo está feito.

---

## 4. Manutenção e Dicas
- Sempre mantenha o campo `usuario` preenchido e atualizado.
- Se um Assessor trocar de usuário, atualize o vínculo no admin.
- Para desativar um Assessor, basta marcar o campo `ativo` como False.
- Não basta adicionar o usuário ao grupo "Assessores"; o vínculo no modelo é obrigatório.
- Se um Assessor trocar de usuário, atualize o vínculo no admin.

---

## 3. Resumo da Lógica
- **Backend:** Verifica vínculo pelo campo `usuario` do modelo Assessor.
- **Frontend:** Exibe módulos conforme o contexto `is_assessor`.
- **Admin:** Cadastro e edição do vínculo são feitos pelo admin do Django.

---

## 6. Exemplo de Código

### Modelo Assessor (resumido)
```python
class Assessor(models.Model):
    usuario = models.OneToOneField(User, ...)
    nome_responsavel = models.CharField(...)
    ativo = models.BooleanField(default=True)
    ...
```

### Serviço de autenticação
```python
class AuthenticationService:
    @staticmethod
    def is_assessor(user):
        return Assessor.objects.filter(usuario=user, ativo=True).exists()
```

### Uso no template
```django
{% if is_assessor %}
    <!-- Exibe apenas Gabinetes -->
{% endif %}
```

---

## 7. Observações
- O vínculo correto garante que o sistema funcione conforme esperado para cada perfil.
- Sempre revise o vínculo no admin em caso de dúvidas sobre permissões ou exibição de módulos.
- Consulte esta documentação para onboarding de novos membros da equipe ou para troubleshooting de acesso de Assessores. 