# Lições Aprendidas — forge-sdd

Padrões de erro já corrigidos, consultados por Builder/Revisor antes de implementar (lido no READ-MIN, feat-01-04). Entradas mais recentes primeiro; o arquivo é aparado automaticamente para respeitar o orçamento.

- Checagem truthy (`if lista:`) em resultado de leitura externa (API/backup) confunde 'lista vazia válida' com 'falha de leitura', deixando cache/estado local travado no último valor não-vazio → Usar checagem explícita de sucesso (`is not None` / `isinstance(x, list)`) em vez de truthy, para toda leitura cujo resultado vazio é um estado legítimo (sdd/features/fix-5362-cache-sheets-zerado-nao-propagado.md)
