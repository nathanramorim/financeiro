# Stack — financeiro

## Dependências

| Camada | Escolha | Versão | Motivo |
|--------|---------|--------|--------|
| Runtime Backend | python | >= 3.11 | Linguagem principal do backend e orquestração de IA |
| Backend Framework | fastapi | >= 0.115.0 | API REST assíncrona, Pydantic v2 e documentação OpenAPI Swagger |
| Servidor ASGI | uvicorn | >= 0.30.0 | Servidor ASGI rápido para produção e desenvolvimento local |
| Runtime Frontend | node.js | >= 20.0.0 | Ambiente de execução para a interface web |
| Frontend Framework | next.js | >= 15.0.0 | React 19 / App Router com SSR/SSG e arquitetura em camadas |
| Estilização | tailwindcss | >= 3.4.0 | Design System mobile-first (`.agents/rules/design-system.md`) |
| Renderização Markdown | react-markdown | >= 9.0.0 | Formatação rica de respostas, cabeçalhos, negritos e listas |
| Package Manager Backend | uv | >= 0.1.0 | Gerenciamento rápido de dependências Python (`pyproject.toml`) |
| Package Manager Frontend | npm | >= 10.0.0 | Gerenciamento de pacotes Node no frontend |
| LLM Gateway | openrouter | - | Comunicação padronizada com múltiplos modelos LLM |
| Persistência | gspread & google-auth | >= 6.0.0 | Manipulação do Google Sheets com cache TTL de 30s e backup local |
| Validação / Schemas | pydantic | >= 2.0.0 | Schemas de entrada e saída da API |

## Layout do projeto
```text
.
├── frontend/                     # Aplicação Frontend Next.js (App Router, Tailwind, TypeScript)
│   ├── src/
│   │   ├── app/                  # Rotas, layouts e páginas (layout.tsx, page.tsx, globals.css)
│   │   ├── components/
│   │   │   ├── ui/               # Componentes atômicos do Design System (Button, Card, Badge, StatTile, Topbar)
│   │   │   ├── chat/             # Componentes de Chat (ChatContainer, MessageBubble, MarkdownRenderer, LoadingIndicator)
│   │   │   ├── transactions/     # Componentes de Transações (TransactionConfirmCard)
│   │   │   └── reports/          # Gráficos responsivos (FinancialCharts)
│   │   ├── domain/               # Modelos e tipagens TypeScript do domínio financeiro
│   │   └── infrastructure/       # Cliente HTTP de comunicação com a API FastAPI
│   ├── package.json              # Scripts e dependências frontend (Next.js na porta 3020)
│   └── tailwind.config.ts        # Tokens de cores e tipografia Montserrat
├── src/                          # Backend Python (FastAPI + Agente)
│   ├── api/                      # Camada de apresentação da API
│   │   ├── main.py               # Instância FastAPI, CORS e middleware
│   │   ├── routes.py             # Rotas REST (/api/chat, /api/transactions, /api/reports, /health)
│   │   └── schemas.py            # Modelos Pydantic de requisição e resposta
│   ├── agent/                    # Orquestração do agente LLM
│   │   ├── engine.py             # Lógica de processamento e detecção de mutações/relatórios
│   │   └── prompts.py            # Instruções e system prompts do agente
│   ├── guardrail/                # Validação de escopo financeiro estrito
│   │   ├── validator.py          # Validador com suporte a relatórios e moedas
│   │   └── rules.py              # Palavras-chave permitidas e mensagens de recusa
│   ├── services/                 # Serviços de integração externa
│   │   └── sheets.py             # Integração Google Sheets com cache TTL (30s) e backup local
│   ├── tools/                    # Ferramentas determinísticas
│   │   ├── expenses.py           # Gestão de despesas fixas e variáveis
│   │   ├── income.py             # Gestão de receitas e saldo
│   │   ├── category.py           # Classificador automático de despesas
│   │   └── math_tool.py          # Operações matemáticas sem alucinação
│   ├── config.py                 # Configurações globais e carregamento do .env
│   └── app.py                    # Streamlit (descontinuado)
├── scripts/
│   └── dev.sh                    # Script executável para inicialização unificada (FastAPI :8000 + Next.js :3020)
└── tests/                        # Suíte de testes automatizados pytest (34 testes)
```

## Comandos Padrão
- **Execução Unificada:** `./scripts/dev.sh`
- **Backend Individual:** `uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload`
- **Frontend Individual:** `npm run dev --prefix frontend` (acesso em `http://localhost:3020`)
- **Testes Backend:** `uv run pytest`
- **Build Frontend:** `npm run build --prefix frontend`
