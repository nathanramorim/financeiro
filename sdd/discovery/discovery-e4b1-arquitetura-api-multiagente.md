# Discovery e4b1 — Conversão e Revisão da Arquitetura da API para Multiagente

## 1. Visão de Produto e Negócio

### 1.1 O Porquê (Motivação)
Atualmente, o backend do assistente financeiro opera sob um modelo mono-agente (`FinancialAgent`), onde um único agente centraliza todas as atribuições:
- Interpretação e classificação de intenções gerais de chat.
- Detecção e extração de transações financeiras (receitas e despesas).
- Cálculo e consolidação de relatórios executivos e categorizações.
- Respostas a dúvidas financeiras, cálculos aritméticos e orientações de economia.

Embora esse design tenha viabilizado o lançamento inicial e as correções com sucesso, ele apresenta limitações crescentes:
1. **Acoplamento e Sobrecarga de Prompt:** Um único prompt precisa cobrir regras de registro, formatação de relatórios, cálculos matemáticos e tom consultivo, aumentando o risco de alucinações e respostas imprecisas.
2. **Dificuldade de Extensão:** Adicionar novas especialidades financeiras (ex: planejador orçamentário, consultor de investimentos, auditor de gastos recorrentes, simulador de dívidas) exige inflar ainda mais a classe mono-agente.
3. **Falta de Especialização e Eficiência:** Diferentes tarefas demandam diferentes estratégias (ex: transações exigem validação determinística rígida; relatórios demandam agregação analítica; consultoria requer raciocínio e empatia).

A conversão para uma **Arquitetura Multiagente Modular e Extensível**:
- Desacopla as responsabilidades em **agentes especializados**, cada qual especialista em um domínio bem delimitado.
- Estabelece um **Roteador/Supervisor Central (Orquestrador)** que direciona a mensagem do usuário ao agente mais qualificado.
- Cria uma **Fórmula Padronizada de Plug-and-Play** (`AgentRegistry` e `BaseAgent`), permitindo que novos agentes sejam implementados e ativados sem alterações no core da API ou nas rotas existentes.

---

### 1.2 Para Quem (Público-Alvo)
- **Usuário Final:** Recebe respostas muito mais precisas, recomendações personalizadas, análises profundas de seus gastos e confirmações transacionais rápidas e seguras.
- **Desenvolvedores / Mantenedores:** Podem criar novos agentes independentes em arquivos isolados, testá-los unitariamente e registrá-los em minutos sem risco de regressão nas demais funcionalidades.
- **Ecossistema do Produto:** Habilita evolução rápida para recursos futuros como inteligência preditiva, metas orçamentárias (Budgeting) e auditoria de faturas.

---

### 1.3 O Como (Macroestratégia)
1. **Padrão Orquestrador / Roteador com Especialistas (Supervisor-Workers):**
   - Um agente supervisor (`AgentRouter` / `SupervisorAgent`) recebe a mensagem já higienizada pelos guardrails.
   - Avalia a intenção da requisição e delega a execução ao agente especializado correspondente.
2. **Catálogo Inicial de Agentes Especializados:**
   - **`TransactionAgent`:** Focado exclusivamente em extração, validação, categorização e confirmação de despesas e receitas.
   - **`ReportAgent`:** Especialista em consolidação de saldos, agregação por categorias, métricas de evolução patrimonial e geração de payloads de gráficos para o frontend.
   - **`AdvisoryAgent`:** Atua como educador e consultor financeiro pessoal, analisando a distribuição de gastos (ex: regra 50/30/20) e oferecendo planos de contenção de despesas.
   - **`GeneralFinancialAgent` (Fallback / Conhecimento):** Responde a dúvidas conceituais de finanças, perguntas gerais e cálculos aritméticos via `MathTool`.
3. **Design Extensível (`Plugin/Registry Pattern`):**
   - Interface abstrata `BaseAgent` definindo contratos estritos de entrada (`AgentContext`), capacidade de atendimento (`can_handle`) e execução (`process`).
   - Registro dinâmico (`AgentRegistry`) permitindo que novos agentes sejam criados em `src/agent/specialists/` e descobertos automaticamente.
4. **Isolamento de Camadas (Clean Architecture):**
   - Manutenção rigorosa das diretrizes de `.agents/rules/arquitetura.md`, mantendo guardrails no domínio, orquestração na aplicação e ferramentas na infraestrutura.
