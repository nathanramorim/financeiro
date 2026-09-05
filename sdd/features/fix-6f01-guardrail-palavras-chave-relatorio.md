# Fix 6f01 — Inclusão de Palavras-Chave de Relatório e Gráficos no Guardrail

## Contexto do Bug
Ao enviar comandos como `"relatorio"`, `"relatório"` ou `"gerar relatório com gráficos"`, o Guardrail rejeitava a mensagem com a mensagem de fora de escopo ("Sua solicitação parece estar fora do escopo financeiro permitido").

## Causas Identificadas
A lista `FINANCIAL_KEYWORDS` em `src/guardrail/rules.py` não continha as palavras "relatorio", "relatório", "grafico", "gráficos", "graficos", "gráfico", "balanço", "balanco", fazendo com que o `GuardrailValidator` classificasse pedidos legítimos de relatórios como fora de escopo.

## Solução Proposta
- Adicionar as palavras-chave relativas a relatórios, gráficos e balanço na constante `FINANCIAL_KEYWORDS` em `src/guardrail/rules.py`.
- Adicionar testes unitários em `tests/test_guardrail.py` garantindo que "relatorio", "relatório" e "gerar relatório com gráficos" passem na validação do Guardrail.

## Critérios de Aceite
- [ ] O comando "relatorio" passa pela validação do Guardrail sem erros.
- [ ] O comando "relatório" passa pela validação do Guardrail sem erros.
- [ ] O comando "gerar relatório com gráficos" passa pela validação do Guardrail sem erros.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
