# Fix b103 — Renderização de Markdown no Chat do Frontend Next.js

## Contexto e Causa Raiz
No frontend Next.js, as mensagens enviadas pelo assistente contendo Markdown (como relatórios com títulos `###`, negritos `**`, listas `-` e itálicos `*`) estavam sendo exibidas com `whitespace-pre-wrap`, exibindo a sintaxe Markdown crua para o usuário final em vez de HTML formatado e estilizado conforme o Design System.

## Escopo da Correção
1. **Componente de Renderização:**
   - Criar ou integrar um renderizador de Markdown no frontend Next.js (ex: `react-markdown` ou parser customizado de Markdown sem injeção de HTML perigoso).
   - Estilizar os elementos renderizados:
     - Títulos `h3` e `h4`: tipografia Montserrat, cores semânticas e espaçamento adequado.
     - Negritos `strong`: fonte com peso 700.
     - Listas com marcadores: alinhamento limpo e espaçamento vertical.
     - Itálicos: estilo discreto para textos de apoio.
2. **Atualização em `MessageBubble.tsx`:**
   - Substituir a tag estática com texto cru pelo componente formatador.
3. **Validação:**
   - Build do Next.js sem erros via `npm run build --prefix frontend`.
   - Testes unitários do backend mantidos 100% aprovados (`uv run pytest`).

## Critérios de Aceite
- [x] O texto em Markdown recebido pelo chat renderiza tags visuais estilizadas (títulos h3/h4, listas, negrito e itálico) sem exibir caracteres crus como `###` ou `**`.
- [x] Build de produção do Next.js aprovado (`npm run build --prefix frontend`).
- [x] Suíte de testes unitários do Python 100% aprovada (`uv run pytest`).
