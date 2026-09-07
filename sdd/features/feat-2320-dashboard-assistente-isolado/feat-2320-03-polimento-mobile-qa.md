# Feature 2320-03 — Polimento Mobile-First e QA

## Contexto e Objetivo
Fechar o discovery 2320 com uma passada de polimento visual e validação manual dos critérios de aceitação definidos em `sdd/discovery/criteria-2320-dashboard-assistente-isolado.md`, garantindo que a navegação Dashboard/Assistente funcione de forma consistente nos breakpoints mobile-first do Design System.

Depende de: `feat-2320-01-navegacao-base.md`, `feat-2320-02-unificacao-dashboard.md`.

## Escopo e Especificações
1. Revisar espaçamentos e safe-area (iOS notch/home indicator) da `BottomNav` fixa.
2. Testar manualmente em 360px, 768px e 1280px (breakpoints do Design System em `.agents/rules/design-system.md`).
3. Validar comportamento do estado do chat (`ChatContainer`) ao alternar entre `/` e `/assistente` — documentar se o histórico é preservado ou reiniciado, e se esse comportamento é aceitável (sem exigir nova lógica de persistência além da já existente no componente).
4. Rodar checklist final contra os 6 critérios de aceitação executáveis de `criteria-2320-dashboard-assistente-isolado.md`.

## Critérios de Aceite
- [ ] Checklist manual dos 6 critérios de aceitação de `criteria-2320-dashboard-assistente-isolado.md` todos validados (360px, 768px, 1280px).
- [ ] `BottomNav` não apresenta sobreposição de conteúdo ou corte por safe-area em dispositivos com notch/home indicator.
- [ ] Comportamento do estado do chat ao trocar de rota documentado no artefato da feature (ou em `sdd/memory/progress.md` no handoff).
- [ ] Nenhuma regressão identificada nas funcionalidades existentes (chat, gráficos, listagem, reconexão offline).
