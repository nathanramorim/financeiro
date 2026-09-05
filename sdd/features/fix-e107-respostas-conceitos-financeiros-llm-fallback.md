# Fix e107 — Respostas a Conceitos Financeiros (LLM Failover e Base Local)

## Contexto e Causa Raiz
Ao perguntar *"o que é taxa selic"*, o assistente respondia com a mensagem genérica *"Recebi sua mensagem financeira e processei as informações com sucesso."*.

### Causas Identificadas:
1. **Rate-limit na OpenRouter (HTTP 429):** O modelo padrão configurado no `.env` (`z-ai/glm-5.2:free`) está sofrendo limitação de taxa (429) no provedor upstream.
2. **Ausência de Failover de Modelos:** `GeneralFinancialAgent` tentava apenas um único modelo. Se ele falhasse, caía direto no fallback genérico.
3. **Fallback Local Vazio de Conteúdo:** O fallback local do `GeneralFinancialAgent` não continha respostas estruturadas para conceitos financeiros fundamentais (Selic, CDI, Reserva de Emergência, Inflação/IPCA, Regra 50/30/20).

## Escopo e Solução
1. **Configuração de Modelo Ativo (`.env`):**
   - Atualizar modelo padrão para `inclusionai/ling-3.0-flash-fin:free` (especializado em finanças e respondendo com status 200).
2. **Failover Automático de Modelos (`src/agent/specialists/general_agent.py`):**
   - Se o modelo configurado retornar 429 ou erro de conexão, tentar automaticamente modelos alternativos disponíveis (`inclusionai/ling-3.0-flash-fin:free`, `minimax/minimax-m3:free`).
3. **Base de Conhecimento Local de Conceitos Financeiros:**
   - Adicionar respostas ricas locais para conceitos fundamentais:
     - **Taxa Selic:** Taxa básica de juros, Copom, impacto em empréstimos e investimentos.
     - **CDI:** Certificado de Depósito Interbancário, benchmark de renda fixa.
     - **Reserva de Emergência:** 3 a 6 meses de custos fixos em liquidez diária.
     - **Inflação / IPCA:** Perda do poder de compra e correção monetária.
     - **Regra 50/30/20:** Divisão orçamentária entre necessidades, desejos e poupança.
4. **Testes Automatizados:**
   - Adicionar testes em `tests/test_specialist_agents.py` validando que perguntas como *"o que é taxa selic"* e *"o que é CDI"* retornam explicações conceituais claras mesmo com LLM mockada ou offline.

## Critérios de Aceite
- [x] Pergunta *"o que é taxa selic"* (e conceitos similares) retorna resposta educativa detalhada (via LLM ou fallback local especializado).
- [x] Failover de modelos LLM implementado em `GeneralFinancialAgent`.
- [x] Testes automatizados cobrem perguntas conceituais em `tests/test_specialist_agents.py`.
- [x] 100% dos testes da suíte passam via `uv run pytest` (60 testes passando).
