# Plan 2320 — Dashboard Unificado & Assistente Isolado

## Roadmap preliminar (quebra sugerida de features)

### Feature A — Navegação base (BottomNav + rotas)
- Criar `components/ui/BottomNav.tsx` (2 itens: Dashboard, Assistente), seguindo Design System.
- Criar `app/assistente/page.tsx` com `ChatContainer` isolado.
- Ajustar `app/layout.tsx` (ou um layout compartilhado) para incluir `Topbar` + `BottomNav` em todas as rotas, com padding-bottom no conteúdo para não sobrepor a nav fixa.
- Critério de pronto: navegar entre `/` e `/assistente` via BottomNav, ambos com Topbar e indicador de status.

### Feature B — Unificação do Dashboard
- Refatorar `app/page.tsx`: remover `activeTab`/controle de abas; renderizar StatTiles → FinancialCharts → Lista de despesas fixas em sequência única.
- Mover o `ChatContainer` para fora de `page.tsx` (passa a viver só em `app/assistente/page.tsx`).
- Validar que `loadData`/polling (15s) continua funcionando na rota `/`.
- Critério de pronto: `/` mobile 360px mostra tudo em um scroll, sem abas.

### Feature C — Polimento mobile-first e QA visual
- Revisar espaçamentos, safe-area (iOS notch) da BottomNav fixa.
- Testar em 360px, 768px, 1280px (breakpoints do Design System).
- Confirmar que estado do chat não se perde de forma perceptível ao alternar rotas (ou documentar comportamento aceito).
- Critério de pronto: checklist de QA manual dos critérios de aceitação do `criteria-2320-dashboard-assistente-isolado.md` todos verdes.

## Estimativa
- Feature A: pequena (1 componente novo + 1 rota nova + ajuste de layout).
- Feature B: pequena/média (refactor de `page.tsx`, sem lógica nova).
- Feature C: pequena (QA/polimento, sem novo código funcional relevante).

## Ordem recomendada
A → B → C (a navegação precisa existir antes de a Feature B poder remover as abas com segurança).
