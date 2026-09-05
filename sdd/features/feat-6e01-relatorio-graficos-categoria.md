# Feature 6e01 — Relatório Financeiro e Gráficos por Categoria

## Contexto e Objetivo
Permitir que o usuário, ao digitar "relatorio" (ou variações como "relatório", "gráficos"), receba um relatório financeiro completo acompanhado de gráficos visuais no Web UI do Streamlit:
1. Gráfico comparativo entre **Total de Receitas** vs **Total de Despesas Mensais**.
2. Gráfico com a **distribuição de despesas por categoria** (ex: Moradia, Alimentação, Transporte, Saúde, Lazer, etc.).

## Requisitos de UX/UI
1. Quando o comando `"relatorio"` ou `"relatório"` for enviado no Chat:
   - O agente gera um resumo executivo com os totais de receita, despesa e saldo.
   - O Web UI (`src/app.py`) detecta os dados do relatório e renderiza componentes gráficos interativos (`st.bar_chart` / `st.pyplot` / `st.area_chart`).
2. Agrupamento por Categoria:
   - Todas as despesas cadastradas são categorizadas e agrupadas pela propriedade `Categoria`.
   - O gráfico por categoria exibe a soma de valores de cada grupo.

## Critérios de Aceite
- [ ] Entradas como "relatorio", "relatório", "relatorio financeiro" disparam a geração do relatório.
- [ ] O resumo textual traz o balanço totalizado de receitas, despesas e saldo líquido.
- [ ] A interface exibe gráficos de barras/pizza para comparativo Receita x Despesa e Distribuição por Categoria.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
