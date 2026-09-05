# Feature e4b1-04 — Extensibilidade, Guia de Novos Agentes e Validação E2E

## Contexto e Objetivo
Garantir que a arquitetura multiagente seja verdadeiramente aberta para extensão e fechada para modificação (Princípio Open/Closed do SOLID e Clean Architecture). Fornecer um agente de demonstração (`BudgetGoalAgent`), guia passo a passo de implementação de novos especialistas, documentação técnica atualizada e validação de ponta a ponta com a interface web.

## Escopo e Especificações
1. **Agente de Exemplo / Extensão (`src/agent/specialists/budget_goal_agent.py`):**
   - Implementar um especialista de exemplo que gerencia metas de economia e orçamento mensal (ex: "quero economizar 500 reais este mês", "qual o status da minha meta?").
   - Demonstrar o fluxo de registro via `AgentRegistry.register(BudgetGoalAgent(...))` sem alterar nenhuma linha de `src/api/routes.py` ou `src/api/main.py`.
2. **Guia de Implementação de Novos Agentes:**
   - Criar `docs/multiagent_guide.md` detalhando:
     - Como herdar de `BaseAgent`.
     - Como implementar o método de afinidade `can_handle`.
     - Como estruturar o retorno em `AgentResult`.
     - Boas práticas de injeção de serviços (`SheetsService`, `MathTool`).
3. **Atualização da Documentação e Regras:**
   - Atualizar `README.md` do repositório explicando a nova topologia multiagente.
   - Atualizar `.agents/rules/arquitetura.md` e `sdd/spec/stack.md` para consolidar o catálogo de agentes e padrões arquiteturais adotados.
4. **Validação Ponta a Ponta (E2E):**
   - Teste manual ou automatizado conectando o frontend Next.js (porta 3020) com o backend FastAPI (porta 8000) executando a nova malha multiagente.
   - Confirmação de que badges, cards de confirmação rápida e gráficos operam com 100% de fluidez.

## Critérios de Aceite
- [x] `BudgetGoalAgent` funcional e registrado dinamicamente sem modificações no core da API.
- [x] Documentação `docs/multiagent_guide.md` criada com exemplos claros de código e passos de homologação.
- [x] Suíte completa de testes executada via `uv run pytest` com 100% de aprovação (54 testes passando).
- [x] Frontend Next.js comunica perfeitamente com a API multiagente sem erros no console ou divergências visuais (build de produção `npm run build` aprovado).
