# Discovery 2320 — Dashboard Unificado & Assistente Isolado

## Porquê
Hoje a home (`frontend/src/app/page.tsx`) mistura três conceitos na mesma tela por abas: StatTiles (sempre visíveis), "Painel & Gráficos" e "Chat com Assistente". Isso obriga o usuário a alternar entre modo de análise (ver dados) e modo de conversa (pedir algo à IA) dentro do mesmo contêiner de abas, o que é confuso em telas pequenas (mobile-first é regra da constituição) e dilui a identidade de cada modo de uso.

## Para quem
Usuário final do app pessoal de finanças, majoritariamente em smartphone, que quer:
- Abrir o app e ver o panorama financeiro (saldo, receitas, despesas, gráficos, despesas fixas) imediatamente, sem precisar trocar de aba.
- Conversar com o assistente (lançar despesas, tirar dúvidas, pedir relatórios) em um espaço dedicado, sem o ruído visual do dashboard.

## Como (macro)
1. **Unificar** StatTiles + FinancialCharts + lista de despesas fixas em uma única tela de Dashboard (`/`), na ordem: Stats → Gráficos → Lista de despesas fixas — sem abas internas, tudo em um único scroll vertical.
2. **Isolar** o Assistente em rota própria (`/assistente`), navegável via barra de navegação inferior fixa (bottom nav), padrão consolidado de UX mobile-first para alternância entre 2 destinos principais.
3. Remover o controle de abas (`activeTab` "chat" | "dashboard") do `page.tsx` atual, substituindo por roteamento Next.js (App Router) com duas rotas de topo.
4. Manter `Topbar` (status online/offline) presente em ambas as rotas, já que é contexto útil tanto no dashboard quanto no chat.

## Decisões confirmadas com o usuário (rodada de clarify)
- **Isolamento do assistente:** rota própria (`/assistente`) + bottom nav fixa — não FAB/drawer, não abas no topo.
- **Ordem do dashboard unificado:** Stats → Gráficos → Lista (mantém a ordem já usada hoje, apenas remove a divisão por abas).

## Fora de escopo
- Alterações no backend FastAPI (rotas, contratos de API) — este discovery é puramente de reorganização de UI/navegação no frontend Next.js.
- Mudanças de conteúdo/lógica do `ChatContainer` ou do `FinancialCharts` além do necessário para movê-los de lugar.
- Autenticação/múltiplos usuários — fora do escopo atual do produto.

## Critérios de sucesso (produto)
- Em uma sessão mobile (360px+), o usuário consegue ver saldo, receitas, despesas, gráficos e despesas fixas em uma única tela de scroll, sem precisar clicar em abas.
- O usuário consegue alternar para o Assistente com um toque (bottom nav), a partir de qualquer uma das duas rotas.
- Nenhuma funcionalidade existente (chat, gráficos, listagem, reconexão com backend offline) é perdida na reorganização.
