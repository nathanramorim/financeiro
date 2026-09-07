# Decisões de Arquitetura (ADRs) — financeiro

## ADR-01: Provedor LLM via OpenRouter
- **Status:** Aceito
- **Contexto:** Necessidade de flexibilidade na escolha de modelos LLM sem acoplamento a um único fornecedor.
- **Decisão:** Utilizar a API do OpenRouter com o SDK `openai` padronizado.
- **Consequência:** Permite chavear entre modelos (ex: Claude, GPT-4o, Llama) ajustando apenas configurações de ambiente.

## ADR-02: Camada Estrita de Guardrail de Entrada
- **Status:** Aceito
- **Contexto:** Garantir a integridade da aplicação e evitar o uso indevido da API para assuntos que não sejam gestão financeira pessoal.
- **Decisão:** Implementar validação antes da chamada principal do modelo, rejeitando requisições fora do domínio.
- **Consequência:** Redução de custos com chamadas LLM e aumento de segurança contra *prompt injection*.

## ADR-03: Persistência de Dados no Google Sheets via API `gspread`
- **Status:** Aceito
- **Contexto:** O usuário deseja que o agente alimente uma planilha no Google Sheets para acompanhamento direto de despesas fixas, receitas e saldo.
- **Decisão:** Usar `gspread` com autenticação OAuth2 / Service Account do Google Cloud.
- **Consequência:** Persistência simples, sem necessidade de hospedar e gerenciar um banco de dados relacional tradicional na fase inicial.

## ADR-04: Módulo de Cálculo Matemático Dedicado (`MathTool`)
- **Status:** Aceito
- **Contexto:** Modelos LLM são propensos a erros de alucinação em operações matemáticas (divisão, multiplicação, parcelamentos).
- **Decisão:** Delegar qualquer conta numérica para execução em código Python nativo via Tool.
- **Consequência:** Garantia de 100% de exatidão nos valores das despesas e saldos.

## ADR-05: Arquitetura Multiagente com Roteador/Supervisor
- **Status:** Aceito
- **Contexto:** O agente mono-agente inicial (`FinancialAgent`) acumulava responsabilidades de transação, relatório, consultoria e cálculo em um único prompt, aumentando risco de alucinação e dificultando extensão.
- **Decisão:** Desacoplar em agentes especialistas (`TransactionAgent`, `ReportAgent`, `AdvisoryAgent`, `BudgetGoalAgent`, `GeneralAgent`), coordenados por um `Router`/Supervisor (`backend/agent/router.py`) com fallback resiliente, seguindo o padrão de registro plug-and-play (`AgentRegistry`, `BaseAgent`).
- **Consequência:** Cada especialista tem prompt e regras focados no seu domínio; novos agentes podem ser adicionados sem alterar rotas ou core da API.
