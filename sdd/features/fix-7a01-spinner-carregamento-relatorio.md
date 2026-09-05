# Fix 7a01 — Otimização do Carregamento de Relatórios e Ocultação de Tool Calls

## Contexto do Bug
Ao solicitar a geração de relatórios, o agente via OpenRouter exibia na tela fragmentos de chamadas pseudo-ferramenta (`<tool_call>...`) antes de renderizar o relatório e gráficos, e a interface não apresentava um indicador visual claro de carregamento durante a consolidação dos dados.

## Causas Identificadas
1. O método `process_message` em `src/agent/engine.py` chamava primeiro a API do OpenRouter antes do fallback local para comandos de relatório, permitindo vazamento de texto bruto da LLM.
2. O `app.py` utilizava uma mensagem genérica de spinner sem personalização de carregamento para geração de relatórios e consolidação de gráficos.

## Solução Proposta
- Garantir no `FinancialAgent.process_message()` o roteamento imediato de solicitações de relatório via `_local_fallback_process()`.
- Exibir spinner customizado `"📊 Processando e gerando relatório financeiro..."` no `src/app.py` durante o processamento do relatório.

## Critérios de Aceite
- [ ] O comando de relatório não exibe tags de `<tool_call>` nem textos intermediários da LLM.
- [ ] A interface exibe spinner de carregamento apropriado durante a geração do relatório.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
