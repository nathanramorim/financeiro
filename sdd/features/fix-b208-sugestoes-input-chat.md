# Fix b208 — Atualização de Sugestões e Preenchimento da Área de Digitação

## Contexto e Problema
1. **Envio Imediato Involuntário:** Ao clicar em um chip de sugestão, o sistema disparava imediatamente o envio para a API (`handleSend(action.cmd)`), sem permitir que o usuário revisasse, editasse o valor/descrição ou decidisse se realmente queria enviar.
2. **Sugestões Desatualizadas:** Os chips exibidos continham apenas ações antigas e não refletiam o novo ecossistema multiagente (Consultoria/Dicas, Metas de Poupança e Conceitos Financeiros).

## Escopo e Solução
1. **Comportamento do Clique nas Sugestões:**
   - Em vez de disparar a mensagem imediatamente, o clique popula o campo de texto (`setInput(text)`) e aplica foco automático no input (`inputRef.current?.focus()`).
   - O usuário tem total controle para revisar, personalizar a mensagem (ex: alterar valor de R$ 150 para outro) e decidir quando pressionar "Enviar" ou a tecla Enter.
2. **Atualização do Catálogo de Sugestões:**
   - Incluir chips para todas as especialidades da malha multiagente:
     - 📊 *Relatório Geral*
     - 💰 *Consultar Saldo*
     - ➕ *Add despesa Mercado R$ 150*
     - 💡 *Como economizar?* (AdvisoryAgent)
     - 🎯 *Minha meta é poupar R$ 1000* (BudgetGoalAgent)
     - 🏦 *O que é taxa Selic?* (GeneralFinancialAgent)
     - 🧮 *Dividir por 2 despesas fixas* (MathTool)
3. **Sugestões Contextuais Dinâmicas:**
   - Quando o assistente responder com `suggested_actions` no payload da API, os chips são atualizados dinamicamente para refletir o contexto do último agente acionado.

## Critérios de Aceite
- [x] Clicar em qualquer chip de sugestão preenche o campo "Digite sua mensagem..." sem disparar o envio automaticamente.
- [x] O campo de input recebe foco automático para digitação após o clique na sugestão.
- [x] O catálogo de sugestões reflete as especialidades multiagente (Transações, Relatórios, Consultoria, Metas e Conceitos).
- [x] Build do frontend Next.js (`npm run build`) validado sem erros de tipagem.
- [x] Suíte de testes automatizados passa via `uv run pytest`.
