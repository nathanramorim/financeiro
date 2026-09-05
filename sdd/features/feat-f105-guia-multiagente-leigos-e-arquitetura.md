# Feature f105 — Guia Multiagente para Leigos, Prompts dos Especialistas e Fluxo Arquitetural

## Contexto e Objetivo
O projeto evoluiu para uma arquitetura multiagente desacoplada e modular. Para garantir que qualquer usuário, gestor de produto ou novo desenvolvedor compreenda com facilidade o funcionamento do sistema, esta feature cria documentações de alta qualidade:
1. **Guia para Leigos (`docs/guia_agentes_para_leigos.md`):** Explicação amigável sobre o que cada agente faz, o que é um prompt de agente, e exemplos práticos de como falar com cada especialista no chat.
2. **Prompts Especializados (`src/agent/prompts.py`):** Centralização e explicitação dos prompts de sistema de cada agente especialista (`TransactionAgent`, `ReportAgent`, `AdvisoryAgent`, `GeneralFinancialAgent`, `BudgetGoalAgent`), definindo a persona, o escopo e as regras individuais de cada um.
3. **Guia de Criação de Novos Agentes (`docs/criando_novos_agentes.md`):** Passo a passo para criar novos especialistas sem tocar nas rotas da API (padrão plug-and-play).
4. **Fluxo Arquitetural Completo (`docs/fluxo_arquitetura_multiagente.md`):** Diagramas visuais em Mermaid e explicação detalhada do trajeto de ponta a ponta da mensagem: *Usuário ➔ Next.js (Porta 3020) ➔ API FastAPI (Porta 8000) ➔ Guardrails ➔ AgentRouter ➔ Especialista Escolhido ➔ Tools/Google Sheets ➔ Resposta Estruturada*.

## Escopo e Especificações
1. **Padronização dos Prompts em `src/agent/prompts.py`:**
   - `TRANSACTION_AGENT_PROMPT`: persona de auditor e extrator rigoroso de lançamentos.
   - `REPORT_AGENT_PROMPT`: persona de analista financeiro executivo.
   - `ADVISORY_AGENT_PROMPT`: persona de consultor financeiro pessoal educador.
   - `GENERAL_AGENT_PROMPT`: persona de assistente geral de dúvidas financeiras.
   - `BUDGET_GOAL_AGENT_PROMPT`: persona de planejador de metas e poupança.
   - Injeção/associação do respectivo prompt na propriedade `system_prompt` de cada especialista em `src/agent/specialists/`.
2. **Guia para Leigos (`docs/guia_agentes_para_leigos.md`):**
   - Linguagem clara sem jargões complexos.
   - Apresentação de cada especialista como um "membro da equipe financeira".
   - Tabela de exemplos de perguntas reais para cada agente.
   - Explicação do que é o prompt ("as instruções de trabalho") de cada agente.
3. **Tutorial de Criação de Novos Agentes (`docs/criando_novos_agentes.md`):**
   - Exemplos de código simples e comentado.
   - Como herdar de `BaseAgent`.
   - Como definir o prompt do novo agente.
   - Como calcular afinidade no `can_handle`.
   - Como registrar no `AgentRouter` dinamicamente.
4. **Fluxo da Arquitetura (`docs/fluxo_arquitetura_multiagente.md`):**
   - Diagrama de sequência e fluxo em Mermaid.
   - Detalhamento de cada estágio da requisição.
   - Explicação do papel dos Guardrails e das ferramentas determinísticas (`MathTool`, `SheetsService`).

## Critérios de Aceite
- [x] Prompts especializados definidos em `src/agent/prompts.py` e associados a cada classe de especialista.
- [x] Documento `docs/guia_agentes_para_leigos.md` criado e formatado com exemplos claros e didáticos.
- [x] Documento `docs/criando_novos_agentes.md` criado com tutorial passo a passo e template reutilizável.
- [x] Documento `docs/fluxo_arquitetura_multiagente.md` criado com diagramas de fluxo Mermaid detalhados.
- [x] 100% dos testes existentes continuam passando via `uv run pytest`.
- [x] Documentação indexada e referenciada no `README.md`.
