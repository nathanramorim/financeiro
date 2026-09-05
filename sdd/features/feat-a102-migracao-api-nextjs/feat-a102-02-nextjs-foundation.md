# Feature a102-02 — Fundação do Frontend Next.js & Design System

## Contexto e Objetivo
Inicializar e estruturar a aplicação frontend em **Next.js (App Router, TypeScript, Tailwind CSS)** dentro de `frontend/`, implementando as diretrizes de Clean Architecture, tokens do Design System (`.agents/rules/design-system.md`) e regras de frontend mobile-first (`.agents/rules/frontend.md`).

## Escopo e Especificações
1. **Estrutura Next.js:**
   - Criação da aplicação em `frontend/` com TypeScript, Tailwind CSS, ESLint.
   - Configuração de paths/alias no `tsconfig.json` (`@/*` apontando para `./src/*`).
2. **Design System & Tipografia:**
   - Fonte Google **Montserrat** aplicada globalmente via `next/font/google`.
   - Configuração do `tailwind.config.ts` com as cores e tokens do Design System (`bg`, `panel`, `panel-border`, `primary`, `success`, `danger`, `warning`, `accent-indigo`, etc.).
3. **Componentes Base (`frontend/src/components/ui/`):**
   - `Button`: Botão acessível com variantes `primary`, `secondary`, `outline`, `danger`, `success` e suporte a full-width em mobile.
   - `Card`: Container padronizado com bordas suaves e cantos arredondados.
   - `Badge`: Pílula de categorização financeira e status.
   - `StatTile`: Card de métrica para Saldo Atual, Total de Receitas e Total de Despesas.
   - `Topbar`: Cabeçalho responsivo com status de conexão e identidade visual.
4. **Layout Mobile-First (`frontend/src/app/`):**
   - Topbar com título do assistente e status online.
   - Layout global com viewport adaptativo para dispositivos móveis (360px a 1280px).

## Critérios de Aceite
- [x] Projeto Next.js compila sem erros via `npm run build` na pasta `frontend/`.
- [x] Componentes base do Design System (`Button`, `Card`, `Badge`, `StatTile`, `Topbar`) implementados e renderizados no layout.
- [x] Layout perfeitamente responsivo (validado em viewports de 360px a 1280px).
