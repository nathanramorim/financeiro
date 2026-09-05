# Plano Preliminar de Implementação — Discovery e4b1: Arquitetura Multiagente da API

## 1. Visão Geral da Quebra de Trabalho (Roadmap)
A evolução do backend de um modelo mono-agente para uma arquitetura multiagente extensível será dividida em 4 fases sequenciais e seguras, garantindo estabilidade e retrocompatibilidade com a API FastAPI e o frontend Next.js já em execução.

---

## 2. Fases e Features Propostas

### Fase 1 — Fundação e Contratos Multiagente (`feat-e4b1-01-core-multiagente`)
- **Objetivo:** Estabelecer as interfaces base, modelos de dados de contexto/resultado e o mecanismo de registro dinâmico.
- **Entregáveis:**
  1. Criação dos contratos `BaseAgent`, `AgentContext` e `AgentResult` em `src/agent/base.py`.
  2. Implementação do `AgentRegistry` em `src/agent/registry.py` com registro explícito e busca por pontuação de capacidade (`can_handle`).
  3. Criação da suíte de testes unitários para o `AgentRegistry` e contratos base.

### Fase 2 — Especialistas de Domínio (`feat-e4b1-02-agentes-especializados`)
- **Objetivo:** Modularizar as responsabilidades hoje acumuladas no mono-agente em agentes especialistas independentes.
- **Entregáveis:**
  1. `TransactionAgent` (`src/agent/specialists/transaction_agent.py`): especializado em detecção, estruturação e confirmação de receitas/despesas.
  2. `ReportAgent` (`src/agent/specialists/report_agent.py`): consolidado financeiro, agregação analítica por categorias e estrutura para gráficos frontend.
  3. `AdvisoryAgent` (`src/agent/specialists/advisory_agent.py`): consultoria sobre boas práticas financeiras, regra 50/30/20 e alertas de gastos.
  4. `GeneralFinancialAgent` (`src/agent/specialists/general_agent.py`): respostas a dúvidas conceituais e operações matemáticas via `MathTool`.
  5. Testes unitários isolados para cada especialista.

### Fase 3 — Supervisor, Roteador e Integração com API (`feat-e4b1-03-supervisor-router-api`)
- **Objetivo:** Implementar o agente supervisor inteligente que avalia a intenção, delega a tarefa e orquestra a resposta para os endpoints da API.
- **Entregáveis:**
  1. Implementação do `AgentRouter` / `SupervisorAgent` em `src/agent/router.py`.
  2. Integração do router nos endpoints `src/api/routes.py`, mantendo total retrocompatibilidade com o frontend Next.js.
  3. Enriquecimento da resposta com metadados do agente executor (`agent_name`, `suggested_actions`).
  4. Testes de integração de rotas com a nova malha multiagente.

### Fase 4 — Extensibilidade e Guia de Novos Agentes (`feat-e4b1-04-guia-extensibilidade`)
- **Objetivo:** Fornecer documentação e modelo de boilerplate para que desenvolvedores adicionem novos agentes sem tocar nas rotas.
- **Entregáveis:**
  1. Criação de exemplo de extensão (ex: `BudgetGoalAgent` ou template documentado).
  2. Documentação no `README.md` e atualização das diretrizes em `sdd/spec/` e `.agents/rules/arquitetura.md`.
  3. Validação de regressão completa (testes de ponta a ponta com Next.js).

---

## 3. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Aumento de latência na classificação de intenções do Supervisor | Médio | Usar heurística rápida combinada com pontuação determinística (`can_handle`), acionando LLM apenas quando a intenção for ambígua. |
| Incompatibilidade com contratos existentes do frontend | Alto | O `AgentResult` preserva os campos esperados pelo frontend (`reply`, `pending_transaction`, `report_data`), apenas enriquecendo com novos metadados opcionais. |
| Falha ou exceção em um agente especializado | Médio | O `AgentRouter` possui cláusula `try/except` com fallback transparente para o `GeneralFinancialAgent`. |
| Concorrência de escrita no Google Sheets | Baixo | Reutilização integral do `SheetsService` já testado com cache TTL de 30s. |
