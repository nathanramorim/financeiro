# Progress — financeiro

## Status
```
Fase 1 — Agente Chat [X] concluído
Fase 2 — API FastAPI + Next.js [X] concluído
Fase 3 — Multiagente & UI [X] concluído
```

## Features ativas
Nenhuma feature ativa no momento. `fix-5362-cache-sheets-zerado-nao-propagado` já mergeado em `main` (PR #4). `feat-2320-dashboard-assistente-isolado` implementada, revisada e validada manualmente pelo usuário em navegador real, aguardando merge do PR #5.

## Próximo passo
- Merge do PR #5.
- Nenhuma feature `pending`/`todo` no índice no momento — próxima ação depende de novo `/discovery`, `/nova-feature` ou `/novo-fix`.

## Handoff da última sessão
- Dashboard (`/`) e Assistente (`/assistente`) agora são rotas separadas do Next.js App Router, navegáveis por uma `BottomNav` fixa (mobile-first). `Topbar` e `BottomNav` vivem no layout raiz (`AppChrome` + `ApiStatusProvider`), compartilhando o status online/offline entre as duas rotas.
- `/` unifica StatTiles → Gráficos → Lista de despesas fixas em um único scroll, sem abas.
- Estado do chat (`ChatContainer`) reinicia ao navegar para `/assistente` (componente desmonta/remonta entre rotas) — comportamento aceito, documentado em `feat-2320-03-polimento-mobile-qa.md`.
- `/revisar` encontrou 3 problemas, todos corrigidos: (1) `env(safe-area-inset-bottom)` não funcionava sem `viewportFit: "cover"` no `layout.tsx`; (2) dashboard buscava dados mesmo com backend offline (agora condicionado a `apiStatus === "online"`); (3) health check duplicado entre `ApiStatusProvider` e `page.tsx` (removido o polling redundante em `page.tsx`).
- `fix-5362`: corrigido bug em `backend/services/sheets.py` — `get_expenses`/`get_incomes`/`_load_backup` agora tratam lista vazia (planilha zerada) como estado válido, propagando ao cache/backup e evitando ressurreição de dado apagado.
