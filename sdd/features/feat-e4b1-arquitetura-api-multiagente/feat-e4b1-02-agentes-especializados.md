# Feature e4b1-02 — Agentes Especialistas de Domínio

## Contexto e Objetivo
Modularizar a lógica do mono-agente existente (`FinancialAgent`) em agentes especialistas independentes e desacoplados, implementando a interface `BaseAgent`. Cada especialista terá responsabilidade única sobre um domínio financeiro específico, garantindo prompts concisos, menor latência, respostas de alta precisão e conformidade com as regras de negócio.

## Escopo e Especificações
1. **`TransactionAgent` (`src/agent/specialists/transaction_agent.py`):**
   - **Responsabilidade:** Extrair valores, descrições, categorias e tipos de transação (despesa vs receita) a partir de mensagens textuais.
   - **Capacidade (`can_handle`):** Detecta gatilhos de gasto/ganho ("gastei", "comprei", "recebi", "pagamento", R$).
   - **Execução (`process`):** Retorna `pending_transaction` estruturado para confirmação do usuário no frontend, utilizando `CategoryTool` para inferir categorias.
2. **`ReportAgent` (`src/agent/specialists/report_agent.py`):**
   - **Responsabilidade:** Gerar relatórios financeiros, saldos líquidos e agregação analítica de despesas por categoria.
   - **Capacidade (`can_handle`):** Detecta solicitações de visão geral ("relatório", "extrato", "resumo", "quanto gastei", "saldo").
   - **Execução (`process`):** Consulta o `SheetsService`, executa agregação analítica determinística (sem alucinações de LLM) e produz a resposta textual formatada em Markdown com o payload `report_data` para gráficos no frontend.
3. **`AdvisoryAgent` (`src/agent/specialists/advisory_agent.py`):**
   - **Responsabilidade:** Oferecer diagnósticos financeiros, dicas personalizadas de contenção de custos e análise baseada em boas práticas (ex: regra orçamentária 50/30/20).
   - **Capacidade (`can_handle`):** Detecta pedidos de conselho ("como economizar", "estou gastando muito", "dica", "planejamento").
   - **Execução (`process`):** Analisa o perfil de despesas recentes via `SheetsService` e devolve orientações práticas e humanizadas.
4. **`GeneralFinancialAgent` (`src/agent/specialists/general_agent.py`):**
   - **Responsabilidade:** Tirar dúvidas conceituais sobre finanças, investimentos básicos, regras de juros e realizar cálculos matemáticos via `MathTool`. Serve também como agente de fallback.
   - **Capacidade (`can_handle`):** Retorna pontuação base (ex: 0.3), garantindo que seja o fallback quando nenhum especialista específico atingir alta afinidade.
5. **Testes Unitários de Especialistas (`tests/test_specialist_agents.py`):**
   - Testar cada especialista de forma isolada com mocks de `SheetsService` e chamadas de LLM.
   - Garantir que `TransactionAgent` gera `pending_transaction` correto.
   - Garantir que `ReportAgent` formata todas as categorias e gera `report_data`.
   - Garantir que operações matemáticas passam estritamente pelo `MathTool`.

## Critérios de Aceite
- [x] 4 agentes especialistas criados sob `src/agent/specialists/`, implementando `BaseAgent`.
- [x] `TransactionAgent` e `ReportAgent` preservam paridade estrita com o comportamento e schemas consumidos pelo frontend.
- [x] Cálculos aritméticos continuam determinísticos via `MathTool` e rotinas analíticas do `ReportAgent`.
- [x] Suíte `tests/test_specialist_agents.py` cobre todos os especialistas com 100% de aprovação no `uv run pytest`.
