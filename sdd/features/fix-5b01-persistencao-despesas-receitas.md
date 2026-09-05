# Fix 5b01 — Correção e Persistência de Adição de Despesas e Receitas

## Contexto do Bug
Ao enviar o comando "add despesa" (ou variações como "add despesa 100" ou "add receita 500"), o agente respondia com texto de confirmação ou com a listagem de despesas, mas não realizava a inclusão real da nova linha no Google Sheets nem no repositório de dados.

## Causas Identificadas
1. O parser do fallback local (`_local_fallback_process` em `src/agent/engine.py`) exigia o termo exato "adicion", ignorando o comando comum "add", fazendo com que "add despesa" caísse no bloco genérico de consulta de despesas.
2. O fallback local não possuía tratamento de intent para adicionar receitas (`IncomeTool.add_income()` / `SheetsService.add_income()`).
3. As chamadas do agente via OpenRouter não possuíam definições de ferramentas (Tool Calling) anexadas ao payload do chat completion, resultando em alucinações de respostas sem a execução efetiva do código Python/SheetsService.

## Solução Proposta
- Ajustar o parser de intenção no fallback local para suportar os padrões "add", "adicionar", "cadastrar", "incluir", "nova despesa", "novo gasto", "add receita", "nova receita", "cadastrar receita".
- Adicionar a extração de descrição e valor para ambas as entidades (despesas e receitas).
- Implementar o método `add_income` em `IncomeTool` integrando com `SheetsService.add_income()`.
- Configurar suporte a Tool Calling no OpenRouter ou fallback idempotente garantindo persistência no `SheetsService`.

## Critérios de Aceite
- [ ] O comando "add despesa [descricao] [valor]" adiciona a linha no Google Sheets/repositório e confirma ao usuário.
- [ ] O comando "add receita [descricao] [valor]" adiciona a linha no Google Sheets/repositório e confirma ao usuário.
- [ ] Suíte de testes unitários atualizada e validada com 100% de sucesso via `uv run pytest`.
