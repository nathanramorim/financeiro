# Feature: Setup Foundation, Streamlit Web Chat e Guardrail

## Metadata
- **ID:** feat-01-01
- **Branch:** `feat/01-agente-financeiro-chat`
- **Fase:** 1
- **Status:** done

## Descrição
Inicializar o projeto Python com `uv`, configurar o ambiente virtual, a estrutura de diretórios em `src/`, a interface gráfica inicial de Web Chat em Streamlit (`src/app.py`) e a camada de Guardrail de escopo (`src/guardrail/`).

## Contexto & Regras Imutáveis
- Gerenciamento de dependências e ambiente exclusivo via `uv` (`uv venv`, `uv add`, `uv run`).
- O Guardrail deve validar se o prompt é do domínio financeiro antes de qualquer processamento posterior.
- Prompts fora de escopo (ex: culinária, código geral, política) devem ser recusados com resposta padrão de bloqueio.

## Arquivos Afetados
- `pyproject.toml`
- `src/app.py`
- `src/config.py`
- `src/guardrail/validator.py`
- `src/guardrail/rules.py`
- `tests/test_guardrail.py`

## Critérios de Aceitação Executáveis
1. **CA-01 (Setup uv):** O comando `uv run pytest` executa os testes sem erros. [PASSED]
2. **CA-02 (Guardrail Aceite):** Prompt *"Quais são minhas despesas fixas deste mês?"* retorna `is_valid = True`. [PASSED]
3. **CA-03 (Guardrail Bloqueio):** Prompt *"Me dê uma receita de bolo de fubá"* retorna `is_valid = False` com mensagem de erro amigável. [PASSED]
4. **CA-04 (Streamlit UI):** A aplicação Streamlit inicia sem erros via `uv run streamlit run src/app.py`. [PASSED]
