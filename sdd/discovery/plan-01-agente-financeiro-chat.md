# Plano de Execução 01 — Agente Financeiro Inteligente

## 1. Roadmap Preliminar de Features

| Feature ID | Nome da Feature | Descrição Breve | Dependências |
|------------|-----------------|-----------------|--------------|
| **feat-01** | `feat-01-foundation-ui-guardrail` | Setup do projeto com `uv`, Streamlit Web Chat basilar e Camada de Guardrail de escopo | Nenhum |
| **feat-02** | `feat-02-openrouter-agent-math` | Integração do Agente LLM via OpenRouter com suporte à `MathTool` para operações aritméticas | feat-01 |
| **feat-03** | `feat-03-sheets-expenses-income` | Repositório Google Sheets (`gspread`), gestão de despesas fixas, receitas e retorno de saldo | feat-02 |
| **feat-04** | `feat-04-categorization-refinement` | Categorizador automático de despesas e refinamento da interface de chat | feat-03 |

## 2. Estimativa de Entregáveis
- **Fase 1 (Fundação):** Ambiente Python com `uv`, interface Streamlit e validação de Guardrail.
- **Fase 2 (Inteligência & Cálculos):** Agente funcional via OpenRouter respondendo no chat e executando divisão/multiplicação de valores sem erros.
- **Fase 3 (Persistência & Negócio):** Conexão total com Google Sheets para gravar/ler despesas fixas e calcular saldo.
- **Fase 4 (Polimento):** Categorização automatizada e validações de borda.

## 3. Próximo Passo
Executar o comando `/split-features` para desdobrar este plano em especificações detalhadas dentro do diretório `sdd/features/feat-01-agente-financeiro-chat/`.
