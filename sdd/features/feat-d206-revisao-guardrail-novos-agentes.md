# Feature d206 — Revisão do Guardrail para Alinhamento com a Malha Multiagente

## Contexto e Objetivo
Com a introdução dos novos agentes especialistas (`AdvisoryAgent`, `BudgetGoalAgent` e `GeneralFinancialAgent`), o assistente financeiro passou a tratar demandas que vão além do simples registro de despesas e receitas. Usuários agora interagem com o sistema para:
- Definir e acompanhar metas orçamentárias (ex: *"quero criar uma meta de economia"*, *"como está minha poupança?"*).
- Pedir conselhos e consultoria financeira pessoal (ex: *"me dê uma dica de planejamento"*, *"estou gastando muito"*, *"como aplicar a regra 50/30/20?"*).
- Tirar dúvidas de mercado e conceitos econômicos (ex: *"o que é taxa Selic ou CDI?"*, *"como montar uma reserva de emergência?"*).

Anteriormente, o `GuardrailValidator` possuía uma lista restrita de palavras-chave (`FINANCIAL_KEYWORDS`), correndo o risco de bloquear perguntas legítimas direcionadas aos novos especialistas quando a frase não continha números ou palavras como "gasto"/"receita".

O objetivo desta feature é revisar e expandir o Guardrail para dar cobertura integral ao vocabulário dos novos especialistas, mantendo intacta a barreira contra perguntas fora de escopo (culinária, futebol, piadas, etc.).

## Escopo e Especificações
1. **Expansão do Vocabulário em `src/guardrail/rules.py`:**
   - **Metas e Poupança (`BudgetGoalAgent`):** `meta`, `metas`, `poupar`, `poupança`, `poupanca`, `reserva`, `teto`, `alvo`, `objetivo`.
   - **Consultoria e Orçamento (`AdvisoryAgent`):** `dica`, `dicas`, `conselho`, `conselhos`, `planejamento`, `economizar`, `gastando`, `cortar`, `50/30/20`, `superávit`, `superavit`, `déficit`, `deficit`, `dívida`, `divida`, `dívidas`, `dividas`.
   - **Mercado e Conceitos Financeiros (`GeneralFinancialAgent`):** `selic`, `cdi`, `investir`, `investimentos`, `juros`, `inflação`, `inflacao`, `rendimento`, `aporte`, `aportes`, `resgate`.
2. **Refinamento do `GuardrailValidator` em `src/guardrail/validator.py`:**
   - Reconhecimento de termos compostos e normalização sem acentos para evitar falsos negativos (ex: "poupança" / "poupanca", "déficit" / "deficit").
   - Preservação estrita das regras de exclusão (`receita de bolo`, `cozinha`, `piada`, `futebol`, etc.).
3. **Testes Automatizados em `tests/test_guardrail.py`:**
   - Testar aprovação de pedidos de metas de economia sem números explícitos.
   - Testar aprovação de pedidos de consultoria financeira e regra 50/30/20.
   - Testar aprovação de dúvidas conceituais de finanças (Selic, CDI, reserva de emergência).
   - Testar permanência do bloqueio em perguntas fora de escopo.

## Critérios de Aceite
- [x] Vocabulário em `src/guardrail/rules.py` expandido para cobrir todas as capacidades dos novos especialistas.
- [x] `GuardrailValidator` aprova com sucesso prompts de consultoria, metas e conceitos financeiros.
- [x] Perguntas não financeiras (culinária, piadas, esportes) continuam bloqueadas com 100% de eficácia.
- [x] Todos os testes da suíte `tests/test_guardrail.py` e testes integrados da API passam sem regressão via `uv run pytest`.
