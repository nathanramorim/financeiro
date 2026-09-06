# feat-c094 — Renomear `src/` para `backend/`

## Contexto
O projeto tem hoje `frontend/` (Next.js) e `src/` (API Python: FastAPI, agentes, guardrail, serviços, ferramentas). A nomenclatura assimétrica (`frontend/` vs `src/`) dificulta o entendimento de qual pasta é qual camada. `frontend/` já tem seu próprio `frontend/src/` interno (padrão Next.js), então a raiz `src/` do projeto é, na prática, o backend.

## Decisão (respostas do usuário)
- Escopo: renomear `src/` → `backend/` na raiz do projeto (não criar aninhamento `backend/src/`).
- Alcance: feature completa — mover arquivos, corrigir todos os imports/referências, rodar suíte de testes, e não deixar quebrado.

## Objetivo
Após a mudança, a estrutura de pastas na raiz deve refletir claramente a divisão frontend/backend:
```
financeiro/
├── backend/     # API Python (FastAPI, agentes, guardrail, services, tools) — antigo src/
├── frontend/    # Next.js
```

## Escopo de arquivos afetados (levantado via grep)
**Código (mover + corrigir imports):**
- `src/__init__.py`, `src/app.py`, `src/config.py`
- `src/agent/**` (engine.py, registry.py, router.py, specialists/*)
- `src/api/**` (main.py, routes.py)
- `src/guardrail/validator.py`
- `src/services/sheets.py`
- `src/tools/expenses.py`, `src/tools/income.py`

**Testes (corrigir imports, não mover — `tests/` fica na raiz):**
- `tests/test_agent_core.py`, `test_agent.py`, `test_api_multiagent.py`, `test_api.py`, `test_category.py`, `test_guardrail.py`, `test_math_tool.py`, `test_sheets_service.py`, `test_specialist_agents.py`

**Scripts/config:**
- `scripts/dev.sh` (`uv run uvicorn src.api.main:app` → `backend.api.main:app`)
- `pyproject.toml` (`pythonpath = ["."]` já cobre — validar se precisa de ajuste)

**Docs / specs (atualizar referências a `src/` para `backend/`):**
- `.agents/rules/arquitetura.md`
- `docs/criando_novos_agentes.md`, `docs/guia_agentes_para_leigos.md`, `docs/multiagent_guide.md`
- `sdd/spec/modules.md`, `sdd/spec/stack.md`
- `sdd/HOWTO.md`
- Specs históricas em `sdd/discovery/*` e `sdd/features/feat-*/fix-*` — **não alterar** (são registro histórico; apenas mencionar a mudança nesta spec).

## Critérios de aceitação
1. Pasta `src/` deixa de existir; `backend/` contém a mesma árvore (agent/, api/, guardrail/, services/, tools/, app.py, config.py, __init__.py).
2. Todos os imports Python (`from src.X import Y`) atualizados para `from backend.X import Y` em código de produção e testes.
3. `scripts/dev.sh` aponta para `backend.api.main:app`.
4. `.agents/rules/arquitetura.md`, `docs/*.md` e `sdd/spec/modules.md`/`stack.md` atualizados para referenciar `backend/` (specs históricas em `sdd/discovery` e `sdd/features` mantidas como estão).
5. Suíte de testes roda 100% verde (`uv run pytest`) após a migração — baseline atual: 60/60 (ver `sdd/memory/progress.md`).
6. `git status` sem arquivos `__pycache__`/`.DS_Store` versionados acidentalmente após o `git mv`.

## Fora de escopo
- Reestruturar o conteúdo interno de `frontend/`.
- Renomear módulos internos (`agent/`, `api/`, `guardrail/`, `services/`, `tools/`) — só a pasta raiz muda de `src` para `backend`.
- Editar specs históricas arquivadas (`sdd/discovery/`, `sdd/features/feat-*` e `fix-*` já concluídas).

## Estratégia de execução sugerida (Builder)
1. `git mv src backend`
2. Atualizar imports com busca/substituição de `from src.` → `from backend.` e `import src.` → `import backend.` em `backend/**/*.py` e `tests/*.py`.
3. Atualizar `scripts/dev.sh`.
4. Atualizar docs listados acima.
5. Rodar `uv run pytest` e corrigir eventuais quebras (ex: `sys.path`/`Path` hardcoded em `backend/app.py`).
