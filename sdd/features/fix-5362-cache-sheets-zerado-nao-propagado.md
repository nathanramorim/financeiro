# fix-5362 — Cache/backup do SheetsService não propaga planilha zerada

## Branch
`fix/5362-cache-sheets-zerado-nao-propagado`

## Contexto
Em `backend/services/sheets.py`, `get_expenses()` e `get_incomes()` só atualizam `_in_memory_db`, o cache de classe (`_cached_expenses`/`_cached_incomes`) e o backup local (`.cache/sheets_backup.json`) quando `if records:` é verdadeiro. Uma lista vazia retornada pelo Google Sheets (planilha zerada pelo usuário) é falsy em Python, então cai no mesmo caminho de "nenhum dado disponível" que uma falha de leitura.

## Bug identificado
1. **Cache nunca "acerta" em estado zerado**: como `_cached_expenses`/`_cached_incomes` nunca chegam a ser setados como `[]` (ficam `None`), toda leitura dentro da janela de TTL (30s) volta a bater na API do Sheets em vez de usar cache — o TTL perde o efeito depois de zerar a planilha.
2. **Backup local fica com dado obsoleto**: `_in_memory_db` e `.cache/sheets_backup.json` continuam com o último estado não-vazio, nunca refletindo a zeragem.
3. **Ressurreição silenciosa de dados apagados**: se uma leitura subsequente falhar por qualquer motivo (rate limit 429, timeout, credencial expirada), o `except` retorna `self._in_memory_db["Despesas"/"Receitas"]` — que ainda contém as transações apagadas pelo usuário no Sheets. O saldo/relatório volta a incluir dados que o usuário removeu, sem nenhum aviso.

## Critérios de aceitação
1. `get_expenses()`/`get_incomes()` distinguem "leitura bem-sucedida retornando lista vazia" de "leitura falhou" — usar `is not None` (ou equivalente) em vez de truthy check em `records`.
2. Uma planilha zerada com sucesso propaga `[]` para `_in_memory_db`, para o cache de classe (`_cached_expenses`/`_cached_incomes` + timestamp) e para o backup local (`_save_backup()`).
3. Após a propagação, uma leitura subsequente dentro do TTL usa o cache (`[]`) sem nova chamada à API — validar com mock contando `worksheet.get_all_records.call_count`.
4. Se uma leitura falhar (exceção) **depois** de a planilha já ter sido observada vazia, o fallback deve devolver `[]` (o último estado real conhecido), não dados antigos anteriores à zeragem.
5. Testes novos em `tests/test_sheets_service.py` cobrindo: (a) planilha zerada propaga corretamente; (b) cache hit funciona também para lista vazia; (c) fallback após exceção não resuscita dado pré-zeragem.
6. Suíte completa continua 100% verde (`uv run pytest`).

## Fora de escopo
- Revisão geral de todo o mecanismo de cache/TTL (só o bug de propagação de lista vazia).
- Mudar o valor do TTL (30s) ou a estratégia de fallback quando não há credenciais.
- Dados-seed hardcoded em `_in_memory_db.__init__` (usados só quando não há credenciais/testes) — permanecem como estão.

## Estratégia de execução sugerida (Builder)
1. Em `get_expenses`/`get_incomes`, trocar `if records:` por checagem que trata `[]` como resultado válido (ex: usar uma sentinela ou `records is not None` com `get_all_records` sempre retornando lista, nunca `None`).
2. Garantir que `_save_backup()` e a atualização do cache de classe rodem também quando `records == []`.
3. Adicionar testes com `MagicMock` simulando `worksheet.get_all_records` retornando `[]` primeiro e depois lançando exceção, validando que o fallback não reintroduz dado antigo.
4. Rodar `uv run pytest`.
