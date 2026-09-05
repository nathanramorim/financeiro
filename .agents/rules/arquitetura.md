# Arquitetura — Clean Architecture & Sistema Desacoplado

O projeto adota uma arquitetura desacoplada com backend em Python (FastAPI) e frontend moderno em Next.js (App Router, TypeScript e Tailwind CSS).

## 1. Backend (Python / FastAPI)
- Localizado em `src/`, gerenciado estritamente com `uv`.
- Organizado em módulos com responsabilidades isoladas:
  - **Presentation / API (`src/api/`):** Rotas FastAPI, controllers REST, modelos Pydantic de request/response e tratamento de CORS/erros.
  - **Application / Agent (`src/agent/`):** Orquestração do assistente (`FinancialAgent`), prompts, histórico e chamadas de ferramentas.
  - **Domain / Guardrails (`src/guardrail/`):** Regras de negócio de segurança e filtro de escopo financeiro estrito.
  - **Infrastructure / Services & Tools (`src/services/`, `src/tools/`):** Integrações externas (`SheetsService` com Google Sheets API, `MathTool` para operações aritméticas determinísticas).
- Regra: Nenhuma operação aritmética é delegada a texto livre de LLM; deve passar pelo `MathTool`. Toda requisição de chat deve ser validada previamente pelos guardrails.

## 2. Frontend (Next.js App Router)
- Localizado no diretório `frontend/` (ou `web/`), seguindo a convenção Next.js `src/`:
  - `src/app/` — Camada de apresentação (rotas, páginas, layout global). Consome hooks e use-cases de aplicação, nunca acessa serviços de infraestrutura diretamente.
  - `src/domain/` — Entidades e contratos de tipos TypeScript de finanças (`Transaction`, `FixedExpense`, `FinancialSummary`, `CategoryReport`), sem dependências externas.
  - `src/application/` — Casos de uso e hooks de orquestração de estado (ex: `useChat`, `useFinancialReports`, `useTransactionConfirmation`). Depende exclusivamente de `domain`.
  - `src/infrastructure/` — Adapters de comunicação HTTP (`apiClient`) consumindo os endpoints da API FastAPI (`/api/chat`, `/api/transactions`, `/api/reports`), implementando contratos do domínio.
- **Hierarquia estrita:** Camadas internas (`domain`, `application`) nunca importam de `presentation` (`src/app`) ou `infrastructure`.

## 3. Distribuição de Componentes Frontend
- `src/components/ui/` — UI compartilhada do Design System: botões, cards, badges, stat tiles, inputs e skeletons, sem lógica de domínio financeiro. Antes de criar um componente novo, verificar se já existe equivalente aqui.
- `src/components/<feature>/` — Componentes específicos de cada fluxo financeiro:
  - `src/components/chat/` — Interface de conversação, bolhas de mensagem, indicador de digitação/loading.
  - `src/components/transactions/` — Cards interativos de confirmação de transações com botões de ação rápida.
  - `src/components/reports/` — Visualização de gráficos financeiros (Receita vs Despesa, Despesas por Categoria).
- Um componente só é promovido para `components/ui/` quando demonstrar reuso em múltiplos fluxos.
