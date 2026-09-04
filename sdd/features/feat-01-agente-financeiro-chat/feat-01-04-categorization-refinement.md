# Feature: Categorização de Despesas e Polimento da Interface

## Metadata
- **ID:** feat-01-04
- **Branch:** `feat/01-agente-financeiro-chat`
- **Fase:** 4
- **Status:** done

## Descrição
Implementar o módulo de categorização de despesas (`src/tools/category.py`) com regras de palavras-chave e fallback inteligente, e refinar a interface de chat Streamlit (`src/app.py`) para exibir dados em tabelas formatadas, métricas de saldo e histórico limpo.

## Contexto & Regras Imutáveis
- Categorias padrão: Moradia, Alimentação, Transporte, Saúde, Lazer, Educação, Outros.
- Interface Web Chat deve formatar respostas financeiras em Markdown com destaque para valores monetários.

## Arquivos Afetados
- `src/tools/category.py`
- `src/app.py`
- `tests/test_category.py`

## Critérios de Aceitação Executáveis
1. **CA-01 (Categorização por Regra):** `CategoryTool.categorize("Supermercado Carrefour")` retorna `"Alimentação"`. [PASSED]
2. **CA-02 (Categorização Padrão):** Descrições desconhecidas recebem `"Outros"` ou sugestão do agente. [PASSED]
3. **CA-03 (UI Polida):** A interface Web exibe cards de saldo (Receitas, Despesas, Balanço) e botões de atalho. [PASSED]
