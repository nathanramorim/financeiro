# Lições Aprendidas — forge-sdd

Padrões de erro já corrigidos, consultados por Builder/Revisor antes de implementar (lido no READ-MIN, feat-01-04). Entradas mais recentes primeiro; o arquivo é aparado automaticamente para respeitar o orçamento.

- env(safe-area-inset-bottom) usado em CSS sem viewportFit: cover no Next.js Viewport resolve sempre para 0 no Safari iOS → Adicionar viewportFit: 'cover' ao export const viewport em app/layout.tsx sempre que algum componente usar env(safe-area-inset-*) (sdd/features/feat-2320-dashboard-assistente-isolado/feat-2320-03-polimento-mobile-qa.md)
