# Assistente Financeiro Inteligente

Sistema inteligente de gestão de finanças pessoais via chat, com validação de escopo por guardrails, integração direta com Google Sheets, cálculos determinísticos via ferramenta matemática e interface moderna mobile-first.

---

## 🏗️ Arquitetura

O projeto adota uma arquitetura desacoplada e Clean Architecture:

- **Backend (Python / FastAPI & Malha Multiagente):**
  - Gerenciado com `uv`.
  - Módulos organizados em camadas (Clean Architecture):
    - `src/api/`: Rotas RESTful (`/api/chat`, `/api/transactions`, `/api/transactions/confirm`, `/api/reports`, `/health`).
    - `src/agent/`: Malha multiagente com `AgentRouter`, `AgentRegistry`, `BaseAgent` e catálogo de especialistas:
      - `TransactionAgent`: Detecção e confirmação de receitas/despesas.
      - `ReportAgent`: Agregação analítica, relatórios e dados para gráficos.
      - `AdvisoryAgent`: Consultoria financeira, regra 50/30/20 e diagnóstico de economia.
      - `GeneralFinancialAgent`: Dúvidas conceituais, operações aritméticas e fallback.
      - `BudgetGoalAgent`: Metas de economia e acompanhamento orçamentário.
    - `src/guardrail/`: Filtro rigoroso de escopo financeiro contra prompts fora de contexto.
    - `src/services/`: Integração com Google Sheets com cache TTL de 30s.
    - `src/tools/`: `MathTool` e `CategoryTool` para operações sem alucinações.
- **Documentação de Referência:**
  - 🧭 [Guia dos Agentes para Leigos](docs/guia_agentes_para_leigos.md) — Quem é cada agente, o que faz e frases de exemplo.
  - 🛠️ [Tutorial: Criando Novos Agentes](docs/criando_novos_agentes.md) — Passo a passo para criar e plugar novos especialistas.
  - 🔄 [Fluxo Completo da Arquitetura](docs/fluxo_arquitetura_multiagente.md) — Diagramas Mermaid e ciclo de vida da requisição.
- **Frontend (Next.js 15 / TypeScript / Tailwind CSS):**
  - Localizado em `frontend/` (porta padrão `3020`).
  - Estruturado em App Router, componentes do Design System (`components/ui/`), componentes de domínio (`components/chat/`, `components/transactions/`, `components/reports/`) e cliente HTTP tipado (`infrastructure/api.ts`).
  - Totalmente adaptado para Mobile-First (responsivo de 360px a 1440px).

---

## 🚀 Como Executar

### 1. Inicialização Unificada (Recomendada)
Para rodar simultaneamente o backend FastAPI na porta `8000` e o frontend Next.js na porta `3020`:
```bash
./scripts/dev.sh
```

### 2. Execução Individual

#### Backend FastAPI:
```bash
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Documentação interativa Swagger disponível em: `http://localhost:8000/docs`

#### Frontend Next.js:
```bash
cd frontend
npm run dev
```
Interface disponível em: `http://localhost:3020`

#### Alternativa Streamlit:
```bash
uv run streamlit run src/app.py
```

---

## 🧪 Testes Automatizados

### Backend (Python):
```bash
uv run pytest
```
Cobre testes unitários do agente, guardrails, math tool, sheets service e integração da API FastAPI.

### Frontend (Next.js):
```bash
cd frontend
npm run build
```
Valida type-check, linting e compilação das páginas e componentes.
