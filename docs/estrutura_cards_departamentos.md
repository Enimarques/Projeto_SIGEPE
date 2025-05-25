# Estrutura e Visual dos Cards de Estatísticas - Página de Departamentos

## Estrutura HTML

- Os cards de estatísticas ficam dentro de um container `.stats-container`.
- Cada card é um `<div>` com as classes `stat-card` e uma classe de cor específica:
  - `stat-card-visitas-hoje`
  - `stat-card-visitas-andamento`
  - `stat-card-total-visitas`
  - `stat-card-visitas-mes`
- Exemplo de card:

```html
<div class="stat-card stat-card-visitas-hoje">
    <i class="fas fa-calendar-day stat-icon"></i>
    <h3>{{ total_visitas }}</h3>
    <p>Total de Visitas</p>
</div>
```

- Os cards são organizados em uma grid Bootstrap:
  - Cada card está dentro de `<div class="col-xl-3 col-md-6 mb-4">` para responsividade.

## Visual e CSS

- **Classe base:** `stat-card`
  - Cor do texto: branco
  - Borda arredondada: 15px
  - Padding: 25px
  - Sombra: `box-shadow: 0 4px 15px rgba(0,0,0,0.1);`
  - Altura fixa: 180px
  - Centralização total (flexbox)
  - Transição suave no hover
  - Efeito hover: elevação e sombra mais forte
- **Título do número:**
  - `<h3>` grande, negrito, sombra de texto
- **Descrição:**
  - `<p>` menor, opacidade 0.9
- **Ícone:**
  - Classe `stat-icon`, tamanho 2rem, opacidade 0.8, cor branca
- **Cores/Gradientes:**
  - `stat-card-visitas-hoje`: `linear-gradient(135deg, #6dd5ed, #2193b0)`
  - `stat-card-visitas-andamento`: `linear-gradient(135deg, #5cb85c, #28a745)`
  - `stat-card-total-visitas`: `linear-gradient(135deg, #f1c40f, #f39c12)`
  - `stat-card-visitas-mes`: `linear-gradient(135deg, #e67e22, #e74c3c)`
- **Responsividade:**
  - Em telas menores, os cards ocupam 100% da largura e reduzem o tamanho do texto/ícone.

## Exemplo Completo

```html
<div class="row mb-4">
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card stat-card-visitas-hoje">
            <i class="fas fa-calendar-day stat-icon"></i>
            <h3>123</h3>
            <p>Total de Visitas</p>
        </div>
    </div>
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card stat-card-visitas-andamento">
            <i class="fas fa-calendar-day stat-icon"></i>
            <h3>45</h3>
            <p>Visitas Hoje</p>
        </div>
    </div>
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card stat-card-total-visitas">
            <i class="fas fa-clock stat-icon"></i>
            <h3>7</h3>
            <p>Visitas em Andamento</p>
        </div>
    </div>
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card stat-card-visitas-mes">
            <i class="fas fa-calendar-alt stat-icon"></i>
            <h3>89</h3>
            <p>Visitas no Mês</p>
        </div>
    </div>
</div>
```

## Observações
- Os cards de estatística são **apenas informativos** (não clicáveis).
- O CSS dos cards de estatística está embutido no próprio template via `{% block extra_css %}`.
- O padrão visual é consistente com os cards de estatística dos gabinetes.
- O layout é responsivo e elegante, com foco em clareza e destaque dos números. 