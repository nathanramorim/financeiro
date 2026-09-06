# Módulos — financeiro

## 1. Web UI (`backend/app.py`)
- Renderização do chat interativo usando Streamlit.
- Manutenção do histórico da sessão de bate-papo.
- Apresentação de respostas formatadas, tabelas de saldo/despesas e alertas de validação do Guardrail.

## 2. Guardrail Module (`backend/guardrail/`)
- Interceptação de mensagens de entrada antes do envio ao modelo LLM.
- Validação de pertinência ao domínio de finanças pessoais (despesas, receitas, saldo, categorização e cálculos).
- Bloqueio de prompts irrelevantes ou maliciosos (*jailbreak*, vazamento de instrução ou desvio de escopo).

## 3. Agente Financeiro & OpenRouter Client (`backend/agent/`)
- Interface de comunicação com o OpenRouter usando client compatível com OpenAI.
- Definição do System Prompt com instruções de comportamento do assistente financeiro.
- Orquestração do ciclo de chamada de ferramentas (*function calling* / *tool use*).

## 4. Módulo de Despesas (`backend/tools/expenses.py`)
- Leitura e consulta de despesas cadastradas no Google Sheets (com foco inicial em despesas fixas).
- Cadastro de novas despesas informando valor, data, descrição, categoria e classificação (fixa/variável).
- Filtros por categoria e período.

## 5. Módulo de Receitas e Saldo (`backend/tools/income.py`)
- Cadastro e consulta de receitas.
- Consolidação e cálculo do saldo atual (Total Receitas - Total Despesas).

## 6. Módulo de Categorização (`backend/tools/category.py`)
- Sugestão e atribuição automática de categorias (ex: Moradia, Alimentação, Transporte, Saúde, Lazer).
- Regras estáticas de palavras-chave com fallback para o modelo LLM.

## 7. Calculadora On-Demand / MathTool (`backend/tools/math_tool.py`)
- Execução segura de expressões aritméticas (multiplicação, divisão por N, aplicação de fatores de ajuste em despesas).
- Garante exatidão matemática exata sem depender do cálculo do texto gerado pela LLM.

## 8. Repositório Google Sheets (`backend/services/sheets.py`)
- Abstração da camada de persistência com `gspread` e autenticação OAuth2 / Service Account.
- Operações CRUD na planilha de controle financeiro.
