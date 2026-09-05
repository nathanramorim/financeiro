# Plano Preliminar de Implementação — Discovery a102: Migração API (FastAPI) e Frontend (Next.js)

## 1. Visão Geral da Quebra de Trabalho (Roadmap)
A migração será executada de forma incremental, mantendo o backend Python funcional a cada etapa e garantindo que o Streamlit continue operando como fallback até que a interface Next.js atinja paridade completa de recursos.

---

## 2. Fases e Features Propostas

### Fase 1 — API Backend FastAPI (`feat-a102-01-fastapi-backend`)
- **Objetivo:** Criar e configurar o servidor FastAPI usando `uv`, expondo a lógica do agente existente.
- **Entregáveis:**
  1. Instalação das dependências (`fastapi`, `uvicorn`, `httpx` para testes) via `uv add`.
  2. Implementação do entrypoint ASGI em `src/api.py`.
  3. Endpoints REST: `/health`, `/api/chat`, `/api/transactions`, `/api/transactions/confirm` e `/api/reports`.
  4. Configuração de CORS para permitir requisições do frontend local.
  5. Testes unitários e de integração de rotas com `TestClient` / `pytest`.

### Fase 2 — Fundação do Frontend Next.js & Design System (`feat-a102-02-nextjs-foundation`)
- **Objetivo:** Inicializar a aplicação Next.js com TypeScript, Tailwind CSS e tokens do Design System.
- **Entregáveis:**
  1. Setup do projeto Next.js (pasta `web/` ou `frontend/`).
  2. Configuração do Tailwind CSS com os tokens e cores de `.agents/rules/design-system.md` (`--primary`, `--panel`, `--panel-border`, etc.).
  3. Configuração da fonte Google **Montserrat**.
  4. Componentes base: Layout principal, Topbar, Eyebrow, Stat Tiles e Chat Container.

### Fase 3 — Experiência do Chat, Confirmações e Gráficos (`feat-a102-03-nextjs-chat-charts`)
- **Objetivo:** Integrar a interface do chat com a API FastAPI, incluindo cartões de confirmação e gráficos.
- **Entregáveis:**
  1. Cliente de API com `fetch` / streaming SSE para `/api/chat`.
  2. Card interativo de confirmação de transação pendente com botões `[✅ Confirmar]` e `[❌ Cancelar]`.
  3. Gráficos de barra responsivos para **Receita vs Despesa** e **Despesas por Categoria** (utilizando Recharts ou Chart.js integrado).
  4. Validação Mobile-First em viewports de 360px a 1440px.

### Fase 4 — Polimento, Homologação e Transição (`feat-a102-04-cutover-homologacao`)
- **Objetivo:** Testes ponta a ponta, documentação e instruções de execução unificadas.
- **Entregáveis:**
  1. Script de inicialização unificado ou comandos no `README.md` (ex: `uv run uvicorn ...` + `npm run dev`).
  2. Atualização da Constituição (`sdd/memory/constitution.md`) refletindo a nova stack (FastAPI + Next.js).
  3. Validação completa do fluxo de ponta a ponta.

---

## 3. Riscos e Mitigações
| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Bloqueio por CORS entre Next.js (3000) e FastAPI (8000) | Médio | Middleware `CORSMiddleware` configurado explicitamente no FastAPI com origins configuráveis via `.env`. |
| Perda de sincronismo com a planilha Google Sheets | Alto | Reuso estrito do `SheetsService` existente com seus 27 testes unitários já aprovados. |
| Complexidade na instalação de Node.js / dependências frontend | Baixo | Uso de scripts npm padrão com documentação no `README.md` e isolamento claro das pastas. |
