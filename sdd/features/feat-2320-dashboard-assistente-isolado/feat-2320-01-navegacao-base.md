# Feature 2320-01 — Navegação Base (BottomNav + Rotas)

## Contexto e Objetivo
Criar a infraestrutura de navegação mobile-first que permitirá isolar o Assistente do Dashboard em rotas separadas do Next.js App Router, acessíveis por uma barra de navegação inferior fixa. Esta feature é pré-requisito para a Feature 2320-02, que remove as abas internas do `page.tsx`.

Referências: `sdd/discovery/discovery-2320-dashboard-assistente-isolado.md`, `sdd/discovery/criteria-2320-dashboard-assistente-isolado.md`.

## Escopo e Especificações
1. **`frontend/src/components/ui/BottomNav.tsx` (novo):**
   - 2 itens fixos: "Dashboard" (rota `/`) e "Assistente" (rota `/assistente`).
   - Item ativo destacado visualmente conforme rota atual (`usePathname` do Next.js).
   - Fixa na base da viewport (`fixed bottom-0`), seguindo Design System (`.agents/rules/design-system.md`).
2. **`frontend/src/app/assistente/page.tsx` (novo):**
   - Renderiza apenas `ChatContainer` (mais Topbar/BottomNav herdados do layout).
   - Reaproveita `checkApiHealth` para manter o indicador de status da Topbar coerente ao entrar direto nesta rota.
3. **`frontend/src/app/layout.tsx` (ajuste):**
   - Incluir `Topbar` e `BottomNav` no layout raiz, para que apareçam em todas as rotas sem duplicação de código por página.
   - Garantir `padding-bottom` no conteúdo principal para a BottomNav fixa não sobrepor conteúdo scrollável (inclui safe-area de iOS notch).

## Critérios de Aceite
- [ ] `/` e `/assistente` são navegáveis via `BottomNav`, sem full page reload (client-side routing).
- [ ] Item ativo da `BottomNav` reflete corretamente a rota atual.
- [ ] `Topbar` com indicador de status (online/offline/checking) presente em ambas as rotas.
- [ ] Nenhum conteúdo é sobreposto pela `BottomNav` fixa em viewport 360px.
- [ ] Nenhuma alteração em `backend/**` (escopo restrito a `frontend/src/**`).
