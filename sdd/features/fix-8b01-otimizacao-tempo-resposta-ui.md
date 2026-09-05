# Fix 8b01 — Otimização do Tempo de Resposta e Fluxo do Streamlit

## Contexto do Bug
O usuário relatou um delay perceptível na resposta do agente e durante o indicador de carregamento (spinner) no Streamlit.

## Causas Identificadas
1. O timeout da requisição HTTP para a API do OpenRouter em `src/agent/engine.py` estava configurado em 30 segundos, retendo a execução quando a API responde com 429 ou está instável antes do fallback local.
2. O arquivo `src/app.py` invocava `st.rerun()` ao gerar relatórios, o que forçava o reprocessamento completo do script do Streamlit do início ao fim, adicionando um ciclo desnecessário de carregamento.

## Solução Proposta
- Reduzir o timeout do `requests.post` em `src/agent/engine.py` para 4 segundos.
- Atualizar o `src/app.py` para renderizar os gráficos de relatórios diretamente na mensagem do assistente dentro do ciclo atual, eliminando a chamada a `st.rerun()`.

## Critérios de Aceite
- [ ] O tempo de resposta para relatórios e comandos locais é praticamente instantâneo.
- [ ] A renderização dos gráficos ocorre diretamente no assistente sem recarregamento extra da página.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
