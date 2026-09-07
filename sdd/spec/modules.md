# Módulos — financeiro

## 1. Web UI (`frontend/`)
- Interface de chat em Next.js (App Router, TypeScript, Tailwind), mobile-first.
- Componentes de chat, confirmação de transações e gráficos de relatório (`components/{chat,transactions,reports,ui}`).
- Comunicação com a API FastAPI via camada `infrastructure/`.

## 2. API REST (`backend/api/`)
- Instância FastAPI, CORS e middleware (`main.py`).
- Rotas REST: `/api/chat`, `/api/transactions`, `/api/reports`, `/health` (`routes.py`).
- Modelos Pydantic de requisição e resposta (`schemas.py`).

## 3. Guardrail Module (`backend/guardrail/`)
- Interceptação de mensagens de entrada antes do envio ao modelo LLM.
- Validação de pertinência ao domínio de finanças pessoais (despesas, receitas, saldo, categorização, relatórios e cálculos).
- Bloqueio de prompts irrelevantes ou maliciosos (*jailbreak*, vazamento de instrução ou desvio de escopo).

## 4. Malha Multiagente (`backend/agent/`)
- `router.py`: Supervisor que roteia a mensagem validada para o agente especialista correto, com fallback resiliente.
- `registry.py`: catálogo dinâmico de agentes especializados.
- `base.py`: contratos `BaseAgent`, `AgentContext` e `AgentResult`.
- `prompts.py`: instruções e system prompts.
- `specialists/`: `transaction_agent.py`, `report_agent.py`, `advisory_agent.py`, `budget_goal_agent.py`, `general_agent.py` — cada um interface de comunicação com o OpenRouter via client compatível com OpenAI, orquestrando o ciclo de *function calling*/*tool use* na sua área de responsabilidade.

## 5. Ferramentas Determinísticas (`backend/tools/`)
- `expenses.py`: leitura, cadastro e filtros de despesas fixas/variáveis no Google Sheets.
- `income.py`: cadastro e consulta de receitas, consolidação do saldo (Total Receitas - Total Despesas).
- `category.py`: sugestão e atribuição automática de categorias (ex: Moradia, Alimentação, Transporte, Saúde, Lazer), regras estáticas com fallback para o modelo LLM.
- `math_tool.py`: execução segura de expressões aritméticas, garantindo exatidão sem depender do texto gerado pela LLM.

## 6. Repositório Google Sheets (`backend/services/sheets.py`)
- Abstração da camada de persistência com `gspread` e autenticação OAuth2 / Service Account.
- Operações CRUD na planilha de controle financeiro, com cache TTL (30s) e backup local em `.cache/sheets_backup.json` resiliente ao erro 429.

## Observação
- `backend/app.py` (Streamlit) está descontinuado; a interface ativa é o frontend Next.js.
