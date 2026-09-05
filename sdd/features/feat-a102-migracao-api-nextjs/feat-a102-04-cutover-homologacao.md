# Feature a102-04 — Homologação E2E, Documentação e Transição

## Contexto e Objetivo
Finalizar a homologação ponta a ponta do sistema desacoplado (FastAPI + Next.js), unificar scripts de execução, documentar o fluxo no `README.md` e alinhar a Constituição do projeto (`sdd/memory/constitution.md`).

## Escopo e Especificações
1. **Validação Ponta a Ponta (E2E):**
   - Teste de fluxo completo: Mensagem do usuário -> Guardrail -> LLM Agent -> Confirmação -> SheetsService -> Atualização de Saldo e Gráficos no Next.js.
   - Suíte completa de 34 testes automatizados em Python passando 100%.
   - Build de produção do Next.js sem erros e sem warnings críticos.
2. **Scripts e Comandos Unificados:**
   - Script `./scripts/dev.sh` executável para iniciar conjuntamente backend e frontend.
   - Comandos documentados no `README.md` para execução individual ou unificada.
3. **Atualização da Documentação:**
   - `sdd/memory/constitution.md` atualizado com FastAPI e Next.js na stack e regras.
   - `sdd/memory/progress.md` e `sdd/features/index.md` atualizados.

## Critérios de Aceite
- [x] Todas as suítes de testes automatizados passam sem falhas (`pytest` e build Next.js).
- [x] Documentação do README e Constituição atualizadas com a nova arquitetura.
- [x] Interface Next.js e API FastAPI funcionais e validadas ponta a ponta.
