# Feature 2320-03 — Polimento Mobile-First e QA

## Contexto e Objetivo
Fechar o discovery 2320 com uma passada de polimento visual e validação manual dos critérios de aceitação definidos em `sdd/discovery/criteria-2320-dashboard-assistente-isolado.md`, garantindo que a navegação Dashboard/Assistente funcione de forma consistente nos breakpoints mobile-first do Design System.

Depende de: `feat-2320-01-navegacao-base.md`, `feat-2320-02-unificacao-dashboard.md`.

## Escopo e Especificações
1. Revisar espaçamentos e safe-area (iOS notch/home indicator) da `BottomNav` fixa.
2. Testar manualmente em 360px, 768px e 1280px (breakpoints do Design System em `.agents/rules/design-system.md`).
3. Validar comportamento do estado do chat (`ChatContainer`) ao alternar entre `/` e `/assistente` — documentar se o histórico é preservado ou reiniciado, e se esse comportamento é aceitável (sem exigir nova lógica de persistência além da já existente no componente).
4. Rodar checklist final contra os 6 critérios de aceitação executáveis de `criteria-2320-dashboard-assistente-isolado.md`.

## Critérios de Aceite
- [x] Checklist manual dos 6 critérios de aceitação de `criteria-2320-dashboard-assistente-isolado.md` todos validados: `npm run build`, `npm run lint` e `tsc --noEmit` verdes; rotas `/` e `/assistente` verificadas via `next dev` (200 OK, BottomNav com item ativo correto, StatTiles/gráficos/lista presentes em `/`, chat isolado em `/assistente`).
- [x] `BottomNav` usa `pb-[env(safe-area-inset-bottom)]` (notch/home indicator) e o conteúdo principal tem `pb-20` no `AppChrome` para não ser sobreposto. Corrigido em revisão: `env(safe-area-inset-bottom)` só é resolvido pelo Safari iOS com `viewport-fit=cover` — adicionado `viewportFit: "cover"` ao `export const viewport` de `frontend/src/app/layout.tsx`, sem o qual o safe-area inset ficava sempre em `0`.
- [x] Comportamento do estado do chat ao trocar de rota: como `/` e `/assistente` são rotas distintas do App Router, o `ChatContainer` desmonta/remonta ao navegar entre elas — o histórico da conversa reinicia (mensagem de boas-vindas) a cada vez que o usuário entra em `/assistente`. Comportamento aceito nesta versão (documentado aqui e no handoff de `progress.md`); persistência de histórico entre navegações fica como possível melhoria futura, fora deste escopo.
- [x] Nenhuma regressão identificada nas funcionalidades existentes (chat, gráficos, listagem, reconexão offline). Corrigido em revisão: `page.tsx` voltou a condicionar `fetchFinancialSummary`/`fetchReports` ao status `online` (via `apiStatus` do `ApiStatusProvider`), evitando requisições fadadas ao erro quando o backend está offline; o botão "Tentar reconectar" agora chama `refreshApiStatus` diretamente (sem duplicar o polling de saúde que já roda no provider). Validação em navegador real confirmada pelo usuário: funcionamento correto.
