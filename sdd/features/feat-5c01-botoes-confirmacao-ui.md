# Feature 5c01 — Botões de Confirmação no Chat Web UI

## Contexto e Objetivo
Permitir que, ao solicitar adição ou atualização de despesas/receitas via Chat, a interface exiba um card de pré-visualização com botões interativos de confirmação (`[✅ Confirmar]`, `[❌ Cancelar]`) antes de efetivar a gravação no Google Sheets/repositório.

## Requisitos de UX/UI
1. Quando uma intenção de mutação (ex: "add despesa Mercado 150" ou "add receita Freelance 500") for detectada:
   - A resposta deve apresentar os detalhes da transação pendente em um card destacado.
   - Apresentar botões de ação interativa no Streamlit (`st.button` ou formulário de confirmação).
2. Ao clicar em **Confirmar**:
   - A ação de inserção/atualização é executada no `SheetsService`.
   - A mensagem no histórico é atualizada/confirmada.
3. Ao clicar em **Cancelar**:
   - A transação é descartada sem gravação no `SheetsService`.

## Critérios de Aceite
- [ ] Mensagens de inclusão/edição exibem o card de pré-confirmação com botões interativos.
- [ ] O clique no botão "Confirmar" grava a alteração no repositório/Sheets e exibe mensagem de sucesso.
- [ ] O clique no botão "Cancelar" descarta a operação.
- [ ] Suíte de testes unitários atualizada e 100% aprovada.
