# Feature: Agente OpenRouter & MathTool (Calculadora Dedicada)

## Metadata
- **ID:** feat-01-02
- **Branch:** `feat/01-agente-financeiro-chat`
- **Fase:** 2
- **Status:** done

## Descrição
Implementar a integração com o OpenRouter usando o SDK `openai` para orquestrar mensagens e chamadas de ferramentas (*tool calling*), e a `MathTool` (`src/tools/math_tool.py`) para resolver operações numéricas (divisão por N, multiplicação por N, rateios) com exatidão determinística.

## Contexto & Regras Imutáveis
- Chave do OpenRouter obtida via variável de ambiente `OPENROUTER_API_KEY` carregada via `python-dotenv`.
- O agente NUNCA deve calcular valores matemáticos em texto livre da LLM; ele deve obrigatoriamente evocar a `MathTool`.
- Execução controlada via `uv`.

## Arquivos Afetados
- `src/agent/engine.py`
- `src/agent/prompts.py`
- `src/tools/math_tool.py`
- `tests/test_math_tool.py`
- `tests/test_agent.py`

## Critérios de Aceitação Executáveis
1. **CA-01 (MathTool - Divisão):** `MathTool.evaluate("200 / 2")` retorna `100.0`. [PASSED]
2. **CA-02 (MathTool - Multiplicação):** `MathTool.evaluate("150 * 3")` retorna `450.0`. [PASSED]
3. **CA-03 (Agent Math Tool Call):** Ao receber *"Divida por 2 a despesa de R$ 500"*, o agente invoca a `MathTool` e responde com `R$ 250.0`. [PASSED]
