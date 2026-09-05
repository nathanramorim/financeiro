# Constituição — financeiro

## Missão
Sistema inteligente de gestão de finanças pessoais via chat web desacoplado, com validação de escopo por guardrails, integração ao Google Sheets com cache resiliente e interface mobile-first moderna.

## Stack
| Camada | Escolha | Motivo |
|--------|---------|--------|
| Runtime Backend | python (>=3.11) | Ecossistema maduro para IA, manipulação de dados e automação |
| Backend Framework | fastapi | API RESTful assíncrona, robusta, tipada e documentada (Porta 8000) |
| Runtime Frontend | node.js (>=20) | Ambiente estável e moderno para a interface web |
| Frontend Framework | next.js (App Router) | Interface moderna exclusiva, modular, TypeScript e performance mobile-first (Porta 3020) |
| Styling UI | tailwindcss | Conformidade estrita com o Design System da organização (`.agents/rules/design-system.md`) |
| Package Manager Backend | uv | Gerenciador rápido de dependências, ambiente virtual e pacotes Python |
| Package Manager Frontend | npm | Gerenciador padrão e estável para ecossistema Node.js / React |
| Gateway LLM | openrouter | Acesso unificado a diversos provedores de modelos de linguagem |
| Persistência | google-sheets | Armazenamento acessível e prático para despesas fixas, receitas e saldo |
| Integração Sheets | gspread / google-auth | Biblioteca Python oficial e estável com cache TTL (30s) e backup local resiliente contra limite 429 |

## Decisões resolvidas
| Decisão | Resolução |
|---------|-----------|
| Arquitetura Desacoplada | Backend em FastAPI expondo rotas REST e Frontend em Next.js com App Router |
| Desativação do Streamlit | Streamlit descontinuado e substituído definitivamente pela interface Next.js |
| Package Manager `uv` | Uso obrigatório e exclusivo de `uv` para gestão de pacotes Python, ambiente virtual e execução (`uv run`, `uv pip`, `uv sync`) |
| OpenRouter Gateway | Centralização do acesso a modelos LLM |
| Guardrail na entrada | Filtragem de prompts fora de contexto antes do envio à LLM |
| Calculadora dedicada | Operações matemáticas executadas em código Python (MathTool) para evitar alucinações |
| Resiliência Google Sheets | Cache TTL em memória (30s) e backup local em `.cache/sheets_backup.json` para eliminar erro 429 de quota |
| Mobile-First Obrigatório | Todas as telas, cards, botões e gráficos do frontend são desenhados prioritariamente para mobile (360px+) |

## Ferramentas e Integrações
| Campo | Valor |
|-------|-------|
| VCS / Work Item System | github |

Consulte `sdd/memory/mcps.md` para o status real de cada MCP configurado (`ativo`/`indisponível`) antes de assumir que ele responde. Se "VCS / Work Item System" for `azure-devops`, use `az repos pr create` (ou instrução equivalente documentada) em vez de `gh pr create`. Se `nenhum`, deixe a branch pronta e informe o usuário, sem tentar nenhum comando de VCS.

## Regras
1. Idioma do chat: Português | Idioma dos commits e PRs: Português
2. Nível de Linguagem: padrão
3. Sem commits diretos em main
4. Branch por feature
5. Uso obrigatório de `uv` para gerenciamento de dependências, ambiente virtual e execução de comandos Python (`uv venv`, `uv run`, `uv pip`, `uv add`)
6. Guardrail obrigatório antes de qualquer processamento principal da LLM
7. Nenhuma operação aritmética deve depender de texto livre da LLM; utilizar ferramenta matemática dedicada (MathTool)
8. Config centralizado em módulo de configuração e secrets em `.env` (nunca commitados)
9. Antes de usar lib externa, consultar context7 com versão exata — desde que `sdd/memory/mcps.md` o liste como `ativo`; se `indisponível`, usar a documentação oficial da lib
10. Toda feature tem critério executável
