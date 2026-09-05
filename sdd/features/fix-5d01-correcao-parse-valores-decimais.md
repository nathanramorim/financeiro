# Fix 5d01 — Correção de Parsing de Valores Decimais com Vírgula/Ponto

## Contexto do Bug
Valores informados com vírgula decimal (ex: `85,5` ou `"85,5"`) ao serem lidos do Google Sheets ou processados pelo agente eram formatados ou convertidos incorretamente como `855.00` em vez de `85.50`.

## Causas Identificadas
1. A conversão de strings numéricas contendo vírgulas decimais em formato brasileiro (ex: `"85,5"`) utilizava casting direto para `float()` ou tratamento que removia a vírgula como separador de milhar, gerando o valor `855.0`.
2. Leitura de registros do Google Sheets pelo `gspread` pode retornar valores como string formatada em pt-BR (com vírgula), causando falha de conversão `ValueError` ou cálculo incorreto.

## Solução Proposta
- Implementar função utilitária unificada `parse_float(val)` que trate de forma consistente inteiros, floats e strings numéricas nos formatos PT-BR (`85,5`, `1.500,50`) e US (`85.5`, `1,500.50`).
- Aplicar `parse_float` na sanitização dos registros lidos e gravados no `SheetsService`, `ExpenseTool`, `IncomeTool` e `FinancialAgent`.
- Adicionar suíte de testes unitários para cobrir todos os formatos decimais e casos de borda com vírgula e ponto.

## Critérios de Aceite
- [ ] O valor `"85,5"` ou `85.5` é lido e exibido corretamente como `R$ 85.50`.
- [ ] O valor `"1.500,50"` ou `1500.50` é lido e exibido corretamente como `R$ 1500.50`.
- [ ] O cálculo de saldo e divisão de despesas fixas respeita os valores decimais exatos.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
