# Feature: Repositório Google Sheets, Gestão de Despesas Fixas e Receitas

## Metadata
- **ID:** feat-01-03
- **Branch:** `feat/01-agente-financeiro-chat`
- **Fase:** 3
- **Status:** done

## Descrição
Desenvolver a camada de persistência `SheetsService` com a biblioteca `gspread`, conectando a planilha Google Sheets para gerir despesas fixas (leitura e cadastro), registrar receitas e retornar o saldo consolidado (Total Receitas - Total Despesas).

## Contexto & Regras Imutáveis
- Autenticação OAuth2 / Service Account configurada via variáveis em `.env`.
- As ferramentas de despesas (`expenses.py`) e receitas/saldo (`income.py`) utilizam o `SheetsService` para persistir alterações.
- Foco inicial da gestão de despesas é em despesas fixas.

## Arquivos Afetados
- `src/services/sheets.py`
- `src/tools/expenses.py`
- `src/tools/income.py`
- `tests/test_sheets_service.py`

## Critérios de Aceitação Executáveis
1. **CA-01 (Leitura de Despesas Fixas):** `ExpenseTool.list_fixed_expenses()` retorna a lista de despesas marcadas como `fixa`. [PASSED]
2. **CA-02 (Cadastro de Despesas):** `ExpenseTool.add_expense("Aluguel", 1500.0, "fixa", "Moradia")` grava uma nova linha no Sheets. [PASSED]
3. **CA-03 (Cálculo de Saldo):** `IncomeTool.get_balance()` retorna o saldo atual calculado a partir da planilha. [PASSED]
