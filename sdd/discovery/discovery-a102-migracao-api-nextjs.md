# Discovery a102 — Migração de Arquitetura: Backend API (FastAPI) e Frontend Moderno (Next.js)

## 1. Visão de Produto e Negócio

### 1.1 O Porquê (Motivação)
Atualmente, o sistema utiliza o **Streamlit** como camada unificada de interface e execução do agente financeiro. Embora excelente para prototipagem rápida, o Streamlit impõe limitações estruturais:
- Ciclo de execução reativo por recarregamento total de script (overhead de ciclo de vida).
- Dificuldade em construir interfaces com alta fidelidade ao Design System (`.agents/rules/design-system.md`), microinterações fluidas e suporte offline/PWA.
- Alto acoplamento entre lógica de agentes/serviços Python e a interface visual.

A migração para uma arquitetura **desacoplada**:
- Transforma os agentes e ferramentas financeiras em uma **API robusta, rápida e reutilizável (FastAPI)** com endpoints REST e streaming (SSE).
- Introduz um **Frontend moderno em Next.js (App Router, React 19/18, Tailwind CSS, TypeScript)**, garantindo conformidade rigorosa com o Design System da organização, performance mobile-first nativa e flexibilidade para novas integrações (ex: apps mobile, widgets, notificações push).

---

### 1.2 Para Quem (Público-Alvo)
- **Usuário Final de Finanças Pessoais:** Deseja uma experiência de chat rápida, responsiva e agradável no celular e desktop, com visualização clara de gráficos, confirmações em 1 clique e histórico persistente.
- **Desenvolvedor / Mantenedor:** Ganha isolamento de responsabilidades: o backend foca na orquestração dos agentes, integração com Google Sheets e guardrails; o frontend foca na experiência de usuário (UX/UI), acessibilidade e responsividade.
- **Sistemas Externos:** Poderão consumir a API financeira independente de interface gráfica.

---

### 1.3 O Como (Macro-estratégia)
1. **Camada Backend (API Python - FastAPI):**
   - Encapsular `FinancialAgent`, `SheetsService`, `GuardrailValidator` e `MathTool` em controladores FastAPI assíncronos.
   - Fornecer endpoints estruturados:
     - `POST /api/chat`: Processamento de mensagens com suporte a streaming Server-Sent Events (SSE).
     - `GET /api/transactions`: Consulta de despesas e receitas cadastradas.
     - `POST /api/transactions/confirm`: Execução confirmada de transações pendentes.
     - `GET /api/reports`: Retorno dos dados agregados para geração de relatórios e gráficos.
     - `GET /health`: Health check e status de conexões externas.
2. **Camada Frontend (Next.js App Router):**
   - Aplicação Next.js configurada na pasta `frontend/` ou repositório complementar.
   - Interface de chat moderna com cards conforme `.agents/rules/design-system.md` (tokens de cores, tipografia Montserrat, botões primários/outline, badges de status).
   - Componentes visuais dedicados para renderização de gráficos (Chart.js ou Recharts) e confirmações de transação (botões primários responsivos).
3. **Estratégia de Coexistência e Transição Suave:**
   - O backend existente em Python permanece como o motor central, garantindo que 100% da lógica de negócio e os 27 testes unitários continuem válidos.
   - O Streamlit continua operacional durante o desenvolvimento do Next.js, permitindo testes comparativos lado a lado até o corte definitivo.
