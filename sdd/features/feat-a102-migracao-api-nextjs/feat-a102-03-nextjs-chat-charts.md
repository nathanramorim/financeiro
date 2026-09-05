# Feature a102-03 — Interface de Chat, Confirmações Interativas e Gráficos

## Contexto e Objetivo
Desenvolver os componentes de domínio e aplicação financeira no Next.js, conectando a interface ao backend FastAPI para conversação com o agente, confirmação em 1 clique de transações e renderização de gráficos responsivos.

## Escopo e Especificações
1. **Camada de Domínio e Infraestrutura HTTP:**
   - `frontend/src/domain/types.ts`: Tipos TypeScript para mensagens, transações, status de confirmação e relatórios.
   - `frontend/src/infrastructure/api.ts`: Cliente HTTP com funções tipadas para:
     - `sendChatMessage(message: string, history?: any[])`
     - `fetchFinancialSummary()`
     - `confirmTransaction(payload: ConfirmTransactionPayload)`
     - `fetchReports()`
2. **Componentes de Chat (`frontend/src/components/chat/`):**
   - `ChatContainer`: Gerenciador de histórico de mensagens, input de envio, scroll automático e botões de atalho rápido.
   - `MessageBubble`: Bolha com estilo diferenciado para Usuário (alinhado à direita, destaque azul) e Assistente (alinhado à esquerda com suporte a markdown, confirmação e gráficos).
   - `LoadingIndicator`: Animação suave de loading durante o processamento do agente.
3. **Card de Confirmação Interativa (`frontend/src/components/transactions/`):**
   - `TransactionConfirmCard`: Exibe detalhes da transação pendente (descrição, categoria, valor formatado em R$) com botões acessíveis `[Confirmar]` e `[Cancelar]`, acionando a API com feedback imediato.
4. **Visualização de Gráficos Financeiros (`frontend/src/components/reports/`):**
   - Gráfico de **Receita vs Despesa** (barras horizontais/verticais com cores semânticas verde/vermelho).
   - Gráfico de **Despesas por Categoria** (distribuição visual por categoria).
   - Totalmente responsivo com largura adaptativa de 100% no mobile.

## Critérios de Aceite
- [x] Envio e recebimento de mensagens do chat funcionando integradamente com o backend FastAPI.
- [x] Card de confirmação de transação permite confirmar inserções diretamente na planilha com feedback em tela.
- [x] Gráficos financeiros renderizam corretamente ao solicitar relatórios ou visualizar resumo.
- [x] Validação mobile-first (elementos utilizáveis com toques em telas touch de 360px+).
