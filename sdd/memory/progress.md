# Progress — financeiro

## Status
```
Fase 1 — Agente Chat [X] concluído
Fase 2 — API FastAPI + Next.js [X] concluído
Fase 3 — Multiagente & UI [X] concluído
```

## Features ativas
Nenhuma feature ativa no momento. `feat-2320-dashboard-assistente-isolado` implementada (3/3 subtarefas), aguardando revisão (`/revisar`) e PR.

## Próximo passo
- Rodar `/revisar` na branch `feat/2320-dashboard-assistente-isolado` antes do merge.
- Validar em navegador real (não coberto por automação nesta sessão): navegação `/` ↔ `/assistente`, safe-area em device com notch, banner offline.

## Handoff da última sessão
- Dashboard (`/`) e Assistente (`/assistente`) agora são rotas separadas do Next.js App Router, navegáveis por uma `BottomNav` fixa (mobile-first). `Topbar` e `BottomNav` vivem no layout raiz (`AppChrome` + `ApiStatusProvider`), compartilhando o status online/offline entre as duas rotas.
- `/` unifica StatTiles → Gráficos → Lista de despesas fixas em um único scroll, sem abas.
- Estado do chat (`ChatContainer`) reinicia ao navegar para `/assistente` (componente desmonta/remonta entre rotas) — comportamento aceito, documentado em `feat-2320-03-polimento-mobile-qa.md`.
