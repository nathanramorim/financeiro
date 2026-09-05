# 🔄 Fluxo Completo da Arquitetura Multiagente

Este documento detalha o ciclo de vida completo de uma mensagem enviada pelo usuário até a renderização visual da resposta na interface, demonstrando a interação entre Next.js, FastAPI, Guardrails, Supervisor e Agentes Especialistas.

---

## 1. Diagrama de Sequência de Ponta a Ponta

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário (Web / Mobile)
    participant Front as Frontend Next.js (:3020)
    participant API as API FastAPI (:8000)
    participant Guard as GuardrailValidator
    participant Router as AgentRouter (Supervisor)
    participant Registry as AgentRegistry
    participant Spec as Agente Especialista
    participant Tools as Tools & Google Sheets

    User->>Front: Digita mensagem no chat (ex: "Add despesa Mercado 150")
    Front->>API: POST /api/chat { message, history }
    
    API->>Guard: validate(message)
    alt Mensagem Fora do Escopo Financeiro
        Guard-->>API: Recusa educada ("Pergunta fora do escopo...")
        API-->>Front: Resposta de bloqueio (is_valid = False)
        Front-->>User: Exibe aviso de escopo financeiro
    else Mensagem Válida de Finanças
        Guard-->>API: Validação Aprovada
        API->>Router: route(AgentContext)
        Router->>Registry: find_best_agent(context)
        Registry-->>Router: Seleciona especialista com maior afinidade (score)
        
        Router->>Spec: process(context)
        
        opt Precisa de Cálculo ou Dados
            Spec->>Tools: Consulta saldo / Agrega categorias / Executa MathTool
            Tools-->>Spec: Retorno determinístico
        end
        
        Spec-->>Router: AgentResult { reply, pending_transaction, report_data, suggested_actions }
        Router-->>API: Retorno padronizado
        API-->>Front: JSON ChatMessageResponse
        Front-->>User: Renderiza resposta em Markdown + Cartão interativo / Gráficos
    end
```

---

## 2. Diagrama de Blocos da Arquitetura (Clean Architecture)

```mermaid
graph TD
    subgraph Presentation_Layer ["1. Camada de Apresentação (Frontend & REST)"]
        UI["🖥️ Frontend Next.js (Porta 3020)<br>App Router + Tailwind CSS"]
        API_Route["⚡ FastAPI /api/chat (Porta 8000)<br>Modelos Pydantic"]
    end

    subgraph Domain_Security ["2. Domínio & Segurança"]
        Guardrail["🛡️ GuardrailValidator<br>Filtro semântico e palavras-chave de finanças"]
    end

    subgraph Application_Multiagent ["3. Aplicação & Malha Multiagente"]
        Router["🧭 AgentRouter (Supervisor)<br>Decide o melhor agente e gerencia contingências"]
        Registry["📚 AgentRegistry<br>Catálogo dinâmico plug-and-play de agentes"]
        
        subgraph Specialists ["Agentes Especialistas"]
            TxAgent["💳 TransactionAgent<br>Parsing de despesas e receitas"]
            RepAgent["📊 ReportAgent<br>Relatórios analíticos e gráficos"]
            AdvAgent["💡 AdvisoryAgent<br>Diagnósticos e regra 50/30/20"]
            GoalAgent["🎯 BudgetGoalAgent<br>Acompanhamento de metas"]
            GenAgent["🧠 GeneralFinancialAgent<br>Conceitos, matemática e fallback"]
        end
    end

    subgraph Infrastructure_Tools ["4. Infraestrutura & Ferramentas"]
        Math["🧮 MathTool<br>Operações aritméticas sem alucinação"]
        Category["🏷️ CategoryTool<br>Classificação automática de despesas"]
        Sheets["📈 SheetsService<br>Google Sheets API com Cache TTL 30s"]
    end

    UI -->|HTTP / JSON| API_Route
    API_Route --> Guardrail
    Guardrail -->|Mensagem Higienizada| Router
    Router --> Registry
    Registry -.-> Specialists
    Router --> TxAgent
    Router --> RepAgent
    Router --> AdvAgent
    Router --> GoalAgent
    Router --> GenAgent
    
    TxAgent --> Category
    TxAgent --> Sheets
    RepAgent --> Sheets
    AdvAgent --> Sheets
    GoalAgent --> Sheets
    GenAgent --> Math
```

---

## 3. As 6 Fases do Ciclo de Vida da Requisição

### Fase 1: Entrada no Frontend (`Next.js` na porta 3020)
- O usuário envia uma mensagem textual na interface responsiva (mobile ou desktop).
- O hook `useChat` empacota a mensagem e o histórico da conversa e dispara uma requisição `fetch` assíncrona para o endpoint `POST /api/chat`.

### Fase 2: Recepção na API (`FastAPI` na porta 8000)
- O controller FastAPI recebe a requisição e valida a estrutura JSON usando o modelo Pydantic `ChatMessageRequest`.
- O CORS configurado permite a comunicação segura entre as origens locais.

### Fase 3: Filtragem de Segurança (`GuardrailValidator`)
- A mensagem é submetida ao validador de escopo financeiro estrito.
- Mensagens fora do contexto financeiro (receitas culinárias, futebol, piadas) são filtradas imediatamente, sem gastar processamento de IA ou serviços externos.

### Fase 4: Descoberta e Roteamento (`AgentRouter` & `AgentRegistry`)
- A mensagem é empacotada em um `AgentContext`.
- O `AgentRouter` aciona o `AgentRegistry.find_best_agent(context)`.
- Cada especialista avalia a mensagem através do método `can_handle(context)` e devolve sua pontuação de afinidade (0.0 a 1.0).
- O agente com maior pontuação é selecionado para executar a tarefa.

### Fase 5: Execução Especializada com Zero Alucinação
- O especialista acionado executa seu método `process(context)`.
- Se a operação envolver matemática, o `MathTool` é utilizado.
- Se envolver persistência ou leitura, o `SheetsService` acessa a planilha (utilizando cache em memória com TTL de 30s para proteger a cota da Google Sheets API).
- Em caso de instabilidade não prevista no especialista, o `AgentRouter` aciona o fallback resiliente com o `GeneralFinancialAgent`, garantindo que a API nunca retorne erro 500 para o usuário.

### Fase 6: Resposta Estruturada e Renderização Visual
- O agente retorna um `AgentResult` contendo:
  - Texto explicativo formatado em Markdown rico (cabeçalhos, negrito, listas, destaques).
  - Dados opcionais de transação pendente (`pending_transaction`), ativando botões interativos `[✅ Confirmar]` e `[❌ Cancelar]`.
  - Dados opcionais de relatório (`report_data`), acionando os gráficos SVG responsivos.
  - Chips de ações sugeridas (`suggested_actions`).
- O frontend Next.js recebe o payload e atualiza a interface instantaneamente.
