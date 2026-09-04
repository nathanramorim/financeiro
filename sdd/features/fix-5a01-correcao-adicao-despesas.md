# Fix 5a01 — Correção do Cadastro de Despesas e Persistência

## Contexto do Bug
Ao enviar mensagens indicando o cadastro de despesas (ex: "adicionei despesa..."), o agente respondia incorretamente com uma listagem mockada de despesas fixas (Aluguel e Internet) e não realizava a adição da despesa informada, tampouco persistia no Google Sheets.

## Causas Identificadas
1. No método `_local_fallback_process` (`src/agent/engine.py`), qualquer mensagem contendo o termo "despesa" disparava a listagem de despesas fixas mockadas (`ExpenseTool.list_fixed_expenses()`).
2. O agente fallback não possuía parser de intent para ação de cadastrar/adicionar despesa (`ExpenseTool.add_expense()`).
3. O fallback em memória de `SheetsService` contém registros pré-definidos que eram retornados sempre que não havia conexão com a API do Google Sheets.

## Solução Proposta
- Implementar tratamento de intenção no agente para reconhecer adição de despesas no fallback local (extraindo valor, descrição e categoria).
- Garantir chamada a `ExpenseTool.add_expense()`.
- Validar tratamento da persistência e log de erro quando a integração com Google Sheets estiver desconfigurada ou ativa.

## Critérios de Aceite
- [ ] Mensagem de adição de despesa dispara `ExpenseTool.add_expense()`.
- [ ] A nova despesa é registrada e confirmada na resposta.
- [ ] Suíte de testes atualizada e passando com `uv run pytest`.
