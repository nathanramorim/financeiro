# Design System — Telas e Dashboards

> Extraído da página `/projetos` do nathanramorim.github.io (os cards de
> Trem de Links, Gestor de Aluguéis, Hub de Agentes, Agenda Isô etc).
> Objetivo: usar esse mesmo visual em qualquer projeto novo, principalmente
> em dashboards e painéis reais, não só em ilustrações de preview.

## Como usar isso

Se o projeto usa o **Forge SDD**, salve este arquivo como
`.agents/rules/design-system.md` na raiz do repositório (é exatamente pra
isso que essa pasta existe: qualquer agente de IA consulta antes de mexer
em UI, sem precisar copiar e colar isso em todo prompt). Se o projeto não
usa Forge SDD, guarde como `docs/design-system.md` e cole o link no início
de qualquer conversa sobre tela nova.

## Princípios

1. **Clareza antes de estilo.** Cards com respiro, hierarquia visual clara
   (título → texto de apoio → ação), sem gradiente ou sombra pesada.
2. **Cor com propósito, não decoração.** Cada cor tem um significado fixo
   (ver tabela de status abaixo) e se repete sempre com o mesmo sentido.
3. **Modo claro por padrão.** Fundo branco, texto escuro, painéis em cinza
   muito claro. Dashboard escuro só se o projeto pedir explicitamente.
4. **Card é a unidade básica.** Quase tudo (item de lista, métrica,
   seção, produto) vira um card com o mesmo tratamento: fundo, borda fina,
   cantos arredondados.

## Tokens (copiar direto)

```css
:root {
  /* base */
  --bg: #ffffff;
  --panel: #f6f8fb;
  --panel-border: #e4e9f0;
  --panel-border-strong: #bfd3f5;
  --text: #0f172a;
  --text-dim: #5b6675;

  /* ação / marca */
  --primary: #2563eb;
  --primary-hover: #1d4ed8;

  /* status */
  --success: #16a34a;
  --success-bg: #dcfce7;
  --warning: #d97706;
  --warning-bg: #fef3c7;
  --danger: #dc2626;
  --danger-bg: #fee2e2;

  /* variedade neutra (avatares, categorias, gráficos) */
  --accent-indigo: #4f46e5;
  --accent-violet: #7c3aed;
  --accent-blue-soft: #60a5fa;
  --accent-blue-softer: #93c5fd;

  --radius: 12px;
  --radius-sm: 8px;
  --radius-pill: 999px;

  --font: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

Import da fonte (Google Fonts):

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap"
/>
```

## Tipografia

| Uso | Peso | Tamanho | Observação |
|---|---|---|---|
| Eyebrow (rótulo acima do título) | 800 | 12px | uppercase, letter-spacing 1.2px, cor `--primary` |
| Título de seção (h1/h2) | 800–900 | 24–32px | cor `--text` |
| Corpo de texto | 400 | 14–16px | cor `--text`, line-height 1.6–1.75 |
| Texto de apoio / legenda | 500–600 | 12–13px | cor `--text-dim` |
| Métrica / valor grande | 800–900 | 20–36px | cor `--primary` ou `--text` |

## Componentes base

### Card / painel

```css
.card {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: var(--radius);
  padding: 20px 22px;
}
.card:hover { border-color: var(--panel-border-strong); }
```

Variante "sobre branco": `background: #fff;` com a mesma borda — usar
quando o card já está dentro de um painel cinza (evita cinza sobre
cinza).

### Badge de status

Sempre a mesma lógica de cor: verde = ativo/sucesso, âmbar =
pendente/atenção, vermelho = erro/pausado, azul = destaque/categoria.

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 700;
}
.badge-success { background: var(--success-bg); color: var(--success); }
.badge-warning { background: var(--warning-bg); color: var(--warning); }
.badge-danger  { background: var(--danger-bg);  color: var(--danger); }
```

### Tag / chip (tecnologia, categoria, hashtag)

```css
.tag {
  font-family: var(--font);
  font-weight: 600;
  font-size: 12px;
  padding: 4px 10px;
  border: 1px solid var(--panel-border-strong);
  border-radius: var(--radius-sm);
  background: #eff4ff;
  color: var(--primary);
}
```

### Botões

```css
.btn-primary {
  background: var(--primary);
  color: #fff;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 700;
}
.btn-primary:hover { background: var(--primary-hover); }

.btn-outline {
  background: #fff;
  color: var(--text);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 700;
}
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
```

### Eyebrow (rótulo em pílula acima do título)

```css
.eyebrow {
  display: inline-flex;
  font-family: var(--font);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--primary);
  background: #eff4ff;
  border: 1px solid var(--panel-border-strong);
  padding: 6px 14px;
  border-radius: var(--radius-pill);
}
```

### Stat tile (número em destaque)

```css
.stat {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: var(--radius-sm);
  padding: 12px 8px;
  text-align: center;
}
.stat-value { font-size: 1.35rem; font-weight: 900; color: var(--primary); }
.stat-label { font-size: 0.68rem; color: var(--text-dim); margin-top: 4px; }
```

## Padrões de dashboard

Esses são os que mais importam pra você — a parte que fez a Agenda Isô
ficar boa.

### Navegação lateral (sidebar)

- Fundo branco, 220–240px de largura, separada do conteúdo por
  `1px solid var(--panel-border)`.
- Item de menu: ícone/dot + label, `padding: 10px 12px`,
  `border-radius: var(--radius-sm)`.
- Item ativo: `background: #eaf1ff; color: var(--primary); font-weight: 600;`.
- Item inativo: `color: var(--text-dim);`.

### Topo da página (dentro do dashboard, não confundir com a "moldura de
produto" abaixo)

- Título da página à esquerda (`h1`/`h2` do padrão de tipografia acima).
- Ação principal à direita, sempre um `.btn-primary` (ex: "+ Novo
  agendamento", "+ Novo agente").

### Card de item de lista (agente, produto, lead, colaborador…)

- Avatar/ícone circular com fundo colorido suave (`--success-bg`,
  `--warning-bg`, tons de azul/indigo claros) — a cor do fundo do avatar
  também pode carregar significado (categoria, tipo).
- Nome em negrito, linha de apoio em `--text-dim` logo abaixo.
- Badge de status no rodapé do card.
- Metadado secundário (contagem, valor, data) como chip cinza neutro:
  `background: #eef2f7; color: var(--text-dim); border-radius: var(--radius-pill);`.

### Pipeline / Kanban (colunas com cards arrastáveis)

- Título da coluna em negrito, 13px, `--text-dim`.
- Divisória vertical entre colunas: `1px solid var(--panel-border)`.
- Card dentro da coluna: mesmo `.card`, mas mais compacto (padding
  12–16px), com avatar pequeno + 2 linhas de texto truncado.
- Coluna final ("fechado", "ganho") pode usar fundo levemente verde
  (`#f0fdf4` com borda `#bbf7d0`) pra sinalizar conclusão sem exagerar.

### Calendário / agenda

- Grid de dias com linhas divisórias sutis (`--panel-border` em 1px,
  opacidade baixa nas linhas internas).
- Evento em destaque: fundo `var(--primary)`, texto branco.
- Evento comum: tons claros de azul (`--accent-blue-soft`,
  `--accent-blue-softer`, ou `#dbeafe`), sem borda.
- Confirmação/feedback (ex: "confirmado via WhatsApp"): card flutuante
  com ícone de check circular em `--primary`, fundo `#f0f6ff`, borda
  `--panel-border-strong`.

### Gráfico de barras simples

- Barras na cor `--primary`, variando opacidade ou usando os tons
  `--accent-blue-soft` / `--accent-blue-softer` pra dar profundidade sem
  precisar de mais de uma cor "de verdade".
- Sem grid de fundo pesado — só uma linha de base (`--panel-border`).
- Nada de 3D, sombra ou gradiente no gráfico.

## "Moldura de produto" (só pra preview/ilustração, não pra tela real)

Quando não tem screenshot real disponível (projeto sem deploy público,
sem terminal à mão pra rodar localmente) e é preciso ilustrar como o
produto funciona — em vez de deixar sem imagem ou usar um print
qualquer, usar essa moldura pra dar contexto de "isso é uma tela de
produto":

```css
.window-frame {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  overflow: hidden;
}
.window-topbar {
  background: #fff;
  border-bottom: 1px solid var(--panel-border);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.window-dot { width: 12px; height: 12px; border-radius: 50%; }
.window-dot.red { background: var(--danger); }
.window-dot.amber { background: var(--warning); }
.window-dot.green { background: var(--success); }
.window-url {
  margin-left: 8px;
  background: #eef2f7;
  border-radius: 8px;
  padding: 4px 12px;
  font-family: monospace;
  font-size: 12px;
  color: var(--text-dim);
}
```

Três bolinhas (vermelho/âmbar/verde, estilo barra de janela) + uma
pílula de "URL" servem de moldura pro conteúdo ilustrado logo abaixo.
Isso é só pra **mockup/preview**, não é um padrão de UI da tela real —
não usar essa barra de bolinhas dentro do produto de verdade.

## Acessibilidade (não negociável)

- `:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }`
  em todo elemento clicável.
- Contraste mínimo AA entre texto e fundo (o par `--text-dim` sobre
  `--panel` já foi validado, evite ficar mais claro que isso pra texto
  de apoio).
- Toda ação (botão de ícone, card clicável) precisa de texto visível ou
  `aria-label`.

## Adaptando por stack

- **CSS puro / Astro** (como o nathanramorim.github.io): colar os tokens
  direto em `:root` e usar as classes acima como referência.
- **Tailwind v3/v4** (hub-agentes, agendaiso, portal-comercial): estender
  as cores do tema em vez de usar classes utilitárias soltas:

  ```js
  // tailwind.config.js
  export default {
    theme: {
      extend: {
        colors: {
          panel: '#f6f8fb',
          'panel-border': '#e4e9f0',
          primary: { DEFAULT: '#2563eb', hover: '#1d4ed8' },
          success: { DEFAULT: '#16a34a', bg: '#dcfce7' },
          warning: { DEFAULT: '#d97706', bg: '#fef3c7' },
          danger: { DEFAULT: '#dc2626', bg: '#fee2e2' },
        },
        borderRadius: { DEFAULT: '12px' },
      },
    },
  };
  ```

- **shadcn/ui + Radix** (hub-agentes, portal-comercial): mapear as
  variáveis de tema do shadcn (`--primary`, `--radius`, `--muted`,
  `--muted-foreground`) pros valores desta tabela, em vez de manter o
  azul/cinza padrão do template.

## Animações (Framer Motion)

Framer Motion é a lib de referência para animações neste design system
em projetos React (Next.js etc).

- **Perguntar antes de incluir.** Framer Motion não é dependência padrão
  de todo projeto. Ao começar uma tela/dashboard novo (ou quando o pedido
  envolver animação/transição), pergunte ao usuário se ele quer usar
  Framer Motion antes de adicionar a dependência ou criar o componente.
- **Movimento com propósito.** Animação reforça hierarquia/feedback
  (entrada de card, transição de página, hover sutil) — não decoração.
  Elementos estáticos (texto de corpo, ícone decorativo) não precisam de
  motion.
- **Duração e easing.** 150–300ms, `ease-out` na entrada / `ease-in` na
  saída. Sem bounce/spring exagerado por padrão — só se pedido
  explicitamente.
- **Acessibilidade.** Respeitar `prefers-reduced-motion` via
  `useReducedMotion()` (ou equivalente) pra reduzir/desativar animação.
- **Padrões comuns:**
  - Entrada de card/seção: fade + leve `translateY`
    (`initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}`).
  - Lista com stagger: `staggerChildren` no container.
  - Transição de página/rota: `AnimatePresence` com fade simples.

## Checklist rápido pra qualquer tela nova

- [ ] Fundo branco ou `--panel`, nunca cinza escuro por padrão.
- [ ] Card com borda fina + `--radius`, sem sombra pesada.
- [ ] Cor de status sempre com o mesmo significado (verde/âmbar/vermelho).
- [ ] Título em Montserrat 800, texto de apoio em `--text-dim`.
- [ ] Botão principal sempre `--primary`, nunca mais de um botão "cheio"
      por seção.
- [ ] Estado de foco visível em todo elemento interativo.
