# Feature e4b1-03 — Supervisor, Roteador e Integração com API

## Contexto e Objetivo
Implementar o Agente Supervisor / Roteador (`AgentRouter`) responsável por avaliar o contexto e intenção da requisição do usuário, selecionar o agente especialista mais qualificado no `AgentRegistry` e delegar a execução de forma assíncrona. Integrar o roteador multiagente nos endpoints da API FastAPI (`src/api/routes.py`), mantendo retrocompatibilidade total com o frontend Next.js e os guardrails de segurança.

## Escopo e Especificações
1. **Agente Supervisor / Roteador (`src/agent/router.py`):**
   - Injetar `AgentRegistry` inicializado com os especialistas padrão.
   - Algoritmo de roteamento:
     1. Recebe `AgentContext` já higienizado pelos guardrails.
     2. Executa seleção rápida por `find_best_agent`. Se houver empate ou baixa confiança (< 0.5), utiliza classificação semântica leve via LLM para desempate.
     3. Invoca `process(context)` no agente selecionado.
     4. Se o especialista levantar exceção, executa fallback gracioso chamando `GeneralFinancialAgent`.
     5. Enriquece o `AgentResult` com tempo de processamento e nome do agente acionado.
2. **Integração com Rotas da API (`src/api/routes.py`):**
   - Atualizar rota `POST /api/chat` para delegar o processamento ao `AgentRouter` ao invés da instância legada mono-agente.
   - Manter retrocompatibilidade estrita do modelo `ChatMessageResponse`:
     - `response: str`
     - `pending_action: Optional[PendingAction]`
     - `is_report: bool`
     - `report_data: Optional[ReportData]`
     - Novos campos opcionais: `agent_name: Optional[str]`, `suggested_actions: Optional[list[str]]`.
   - Garantir que o endpoint continue validando através de `GuardrailValidator` antes do roteador.
3. **Testes de Integração da API (`tests/test_api_multiagent.py`):**
   - Validar chamadas a `/api/chat` para diferentes intenções (registro de transação, pedido de relatório, conselho financeiro, dúvida geral).
   - Validar que a resposta JSON mantém a estrutura esperada pelo frontend Next.js.
   - Validar comportamento em cenários de exceção com fallback.

## Critérios de Aceite
- [x] `AgentRouter` orquestra dinamicamente os agentes especialistas com seleção baseada em pontuação e fallback resiliente.
- [x] Endpoint `/api/chat` consome a arquitetura multiagente sem introduzir quebra de contrato para o frontend Next.js.
- [x] Todos os 34 testes existentes continuam passando sem regressões.
- [x] Suíte `tests/test_api_multiagent.py` adicionada e validada com 100% de aprovação via `uv run pytest`.
