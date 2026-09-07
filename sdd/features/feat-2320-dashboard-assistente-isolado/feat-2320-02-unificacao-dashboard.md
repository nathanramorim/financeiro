# Feature 2320-02 — Unificação do Dashboard

## Contexto e Objetivo
Remover o controle de abas ("Chat" | "Painel & Gráficos") de `frontend/src/app/page.tsx` e consolidar StatTiles + FinancialCharts + Lista de despesas fixas em uma única tela de scroll vertical, na ordem definida no discovery: Stats → Gráficos → Lista. O `ChatContainer` sai desta rota e passa a viver exclusivamente em `/assistente` (Feature 2320-01).

Depende de: `feat-2320-01-navegacao-base.md` (a rota `/assistente` precisa existir antes de remover o chat daqui).

## Escopo e Especificações
1. **`frontend/src/app/page.tsx` (refactor):**
   - Remover estado `activeTab` e o bloco de botões de abas.
   - Remover a renderização condicional do `ChatContainer` (migrado para `/assistente`).
   - Renderizar sempre, em sequência única: `StatTile` (saldo/receitas/despesas) → `FinancialCharts` → Card de "Despesas Fixas Cadastradas".
   - Manter o banner de aviso de backend offline e o botão "Tentar reconectar".
   - Manter `loadData`/polling de 15s (`useEffect` + `setInterval`) sem alterações de lógica.
2. Nenhuma mudança nos componentes `StatTile`, `FinancialCharts`, `Card`, `Badge`, `Button` — apenas reorganização de composição em `page.tsx`.

## Critérios de Aceite
- [ ] `/` em viewport 360px exibe, em um único scroll, sem abas: StatTiles → Gráficos → Lista de despesas fixas.
- [ ] `ChatContainer` não é mais renderizado em `/` (só existe em `/assistente`).
- [ ] Polling de dados (`fetchFinancialSummary`, `fetchReports`, 15s) continua funcionando normalmente em `/`.
- [ ] Banner de erro/reconexão quando backend offline continua funcional.
- [ ] Nenhuma alteração em `backend/**`.
