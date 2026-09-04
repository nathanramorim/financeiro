# Stack — financeiro

## Dependências

| Camada | Escolha | Versão | Motivo |
|--------|---------|--------|--------|
| Runtime | python | >= 3.11 | Linguagem principal do projeto |
| Package Manager | uv | >= 0.1.0 | Gerenciamento rápido de dependências, `pyproject.toml` e `uv.lock` |
| Web UI | streamlit | >= 1.30.0 | Interface de Web Chat interativa e rápida |
| LLM Gateway | openai (OpenRouter Client) | >= 1.0.0 | Comunicação padronizada via API OpenAI/OpenRouter |
| Persistência | gspread & google-auth | >= 6.0.0 | Manipulação da planilha Google Sheets via OAuth2 / Service Account |
| Validação / Schemas | pydantic | >= 2.0.0 | Schemas de entrada, saída e tipagem de dados |
| Config / Env | python-dotenv | >= 1.0.0 | Carregamento de variáveis de ambiente do `.env` |

## Layout do projeto
```text
src/
├── app.py               # Entrypoint da aplicação Streamlit Web Chat
├── config.py            # Carregamento centralizado de configurações e variáveis .env
├── guardrail/           # Camada de validação de escopo financeiro e segurança
│   ├── validator.py     # Filtro de relevância e segurança de prompts
│   └── rules.py         # Definição de regras de escopo financeiro
├── agent/               # Agente LLM financeiro e cliente OpenRouter
│   ├── engine.py        # Loop de conversação e orquestração de tool calls
│   └── prompts.py       # System prompts e definições de instruções do agente
├── tools/               # Ferramentas executadas pelo agente
│   ├── expenses.py      # Gestão e consulta de despesas (fixas e variáveis)
│   ├── income.py        # Gestão de receitas e consolidação de saldo
│   ├── category.py      # Categorização e classificação de gastos
│   └── math_tool.py     # Calculadora segura (divisão, multiplicação e rateios)
└── services/            # Camada de integração externa
    └── sheets.py        # Repositório de dados integrado ao Google Sheets (gspread/MCP)
```

## Comandos Padrão (uv)
- **Criar/ativar ambiente:** `uv venv`
- **Instalar dependência:** `uv add <pacote>`
- **Executar aplicação:** `uv run streamlit run src/app.py`
- **Executar testes:** `uv run pytest`
