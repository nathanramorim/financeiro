# Feature a102-01 — Backend API com FastAPI

## Contexto e Objetivo
Implementar o backend desacoplado com **FastAPI** para o sistema financeiro, expondo a inteligência do agente, guardrails, serviços de integração com Google Sheets e ferramentas matemáticas através de endpoints REST assíncronos e documentados.

## Escopo e Especificações
1. **Dependências:**
   - Adicionar `fastapi`, `uvicorn[standard]` e `httpx` (para testes) via `uv add`.
2. **Estrutura de API (`src/api/`):**
   - `src/api/main.py`: Inicialização da aplicação FastAPI com tags de documentação, prefixo `/api` e middleware `CORSMiddleware` (permitindo origens locais como `http://localhost:3000`).
   - `src/api/schemas.py`: Modelos Pydantic para request/response:
     - `ChatMessageRequest(message: str, history: Optional[list[dict]])`
     - `ChatMessageResponse(response: str, pending_action: Optional[PendingAction], is_report: bool, report_data: Optional[ReportData])`
     - `ConfirmTransactionRequest(action: str, descricao: str, valor: float, categoria: Optional[str], tipo: Optional[str])`
     - `TransactionItem(descricao: str, valor: float, tipo: Optional[str], categoria: Optional[str])`
     - `FinancialSummaryResponse(total_receitas: float, total_despesas: float, saldo_liquido: float, fixed_expenses: list[TransactionItem], incomes: list[TransactionItem], despesas_por_categoria: dict[str, float])`
   - `src/api/routes.py`:
     - `GET /health`: Retorna status do serviço (`{"status": "ok", "app": "financeiro-api"}`).
     - `POST /api/chat`: Processa a mensagem pelo `GuardrailValidator` e `FinancialAgent`, retornando a resposta, ações pendentes e dados para gráficos.
     - `GET /api/transactions`: Lista despesas fixas, receitas e saldo atual consultando `SheetsService`.
     - `POST /api/transactions/confirm`: Executa a inserção confirmada de despesa ou receita via `SheetsService`.
     - `GET /api/reports`: Retorna sumário financeiro com totais categorizados para renderização de gráficos.
3. **Testes Automatizados (`tests/test_api.py`):**
   - Testes de todos os endpoints com `TestClient(app)`.
   - Mocking de `SheetsService` e `FinancialAgent` para testes isolados e reproduzíveis.

## Critérios de Aceite
- [x] Servidor FastAPI inicializa com sucesso em `uv run uvicorn src.api.main:app`.
- [x] Endpoints `/health`, `/api/chat`, `/api/transactions`, `/api/transactions/confirm` e `/api/reports` respondem conforme esquemas Pydantic.
- [x] Suíte de testes `tests/test_api.py` cobre todos os endpoints com 100% de aprovação via `uv run pytest`.
