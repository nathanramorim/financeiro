# Critérios Técnicos — Discovery e4b1: Arquitetura de API Multiagente Modular e Extensível

## 1. Visão Técnica e Arquitetural (C4 Model)

### 1.1 Diagrama de Contexto de Sistema (C4 - Nível 1)
```mermaid
C4Context
    title Diagrama de Contexto - Sistema Financeiro Inteligente Multiagente

    Person(user, "Usuário", "Gerencia finanças pessoais pelo chat interativo (web/mobile).")
    
    System(financeiro_system, "Sistema Financeiro IA (Multiagente)", "Orquestra múltiplos agentes especializados para registro, relatórios, auditoria e consultoria financeira.")
    
    System_Ext(google_sheets, "Google Sheets API", "Persistência tabular de transações e categorias.")
    System_Ext(openrouter, "OpenRouter LLM Gateway", "Modelos de linguagem para raciocínio, intenções e respostas especializadas.")

    Rel(user, financeiro_system, "Interage via chat, consulta relatórios e confirma lançamentos", "HTTPS / JSON")
    Rel(financeiro_system, google_sheets, "Lê e grava receitas, despesas e categorias", "OAuth2 / gspread (com cache TTL)")
    Rel(financeiro_system, openrouter, "Inferência e roteamento de agentes especializados", "HTTPS REST")
```

---

### 1.2 Diagrama de Contêineres (C4 - Nível 2)
```mermaid
C4Container
    title Diagrama de Contêineres - Arquitetura Multiagente Desacoplada

    Person(user, "Usuário", "Interage com o frontend.")

    Container(frontend_app, "Frontend Web (Next.js)", "Next.js 15, React, TypeScript, Tailwind CSS", "Interface com chat, cards de confirmação rápida e gráficos interativos.")
    
    Container(backend_api, "Backend API (FastAPI)", "Python 3.12, FastAPI, UV", "Exponibiliza endpoints REST e orquestra a malha de agentes especializados.")

    ContainerDb_Ext(sheets_db, "Planilha Google Sheets", "Google Sheets", "Base de dados tabular.")
    System_Ext(openrouter_api, "OpenRouter Gateway", "API externa", "Provedor LLM.")

    Rel(user, frontend_app, "Usa interface web", "HTTPS")
    Rel(frontend_app, backend_api, "Chama endpoints /api/chat, /api/reports, /api/transactions", "HTTP / JSON")
    Rel(backend_api, sheets_db, "Operações CRUD", "gspread (Cache 30s)")
    Rel(backend_api, openrouter_api, "Roteamento e inferência de agentes", "HTTPS REST")
```

---

### 1.3 Diagrama de Componentes do Backend (C4 - Nível 3)
```mermaid
C4Component
    title Diagrama de Componentes - Malha Multiagente do Backend

    Container_Boundary(api_boundary, "Backend FastAPI (src/)") {
        Component(routes, "API Routers", "src/api/routes.py", "Controladores REST (/api/chat, /api/transactions, /api/reports)")
        Component(guardrail, "Guardrail Validator", "src/guardrail/", "Garante escopo financeiro estrito antes de invocar agentes")
        
        Component(router, "Agent Supervisor / Router", "src/agent/router.py", "Classifica a intenção e delega para o agente especializado mais adequado")
        Component(registry, "Agent Registry", "src/agent/registry.py", "Catálogo dinâmico de agentes registrados (Plug-and-play)")
        
        Component(tx_agent, "TransactionAgent", "src/agent/specialists/transaction_agent.py", "Extração, parsing e confirmação de receitas/despesas")
        Component(rep_agent, "ReportAgent", "src/agent/specialists/report_agent.py", "Cálculo de saldos, agregação de categorias e payloads de gráficos")
        Component(adv_agent, "AdvisoryAgent", "src/agent/specialists/advisory_agent.py", "Consultoria financeira, regras de orçamento e dicas de economia")
        Component(gen_agent, "GeneralFinancialAgent", "src/agent/specialists/general_agent.py", "Dúvidas gerais, conceitos e fallback")

        Component(sheets_svc, "SheetsService", "src/services/sheets.py", "Gerenciamento de leitura e escrita no Google Sheets com cache TTL")
        Component(math_tool, "MathTool", "src/tools/math_tool.py", "Operações aritméticas determinísticas")
    }

    Rel(routes, guardrail, "Valida mensagem", "Python Call")
    Rel(guardrail, router, "Encaminha mensagem validada", "AgentContext")
    Rel(router, registry, "Consulta agentes ativos", "list[BaseAgent]")
    
    Rel(router, tx_agent, "Delega se intenção de transação", "process(context)")
    Rel(router, rep_agent, "Delega se intenção de relatório/saldo", "process(context)")
    Rel(router, adv_agent, "Delega se intenção consultiva/orçamento", "process(context)")
    Rel(router, gen_agent, "Fallback para dúvidas gerais", "process(context)")

    Rel(tx_agent, sheets_svc, "Registra transação", "add_expense / add_income")
    Rel(rep_agent, sheets_svc, "Consulta dados agregados", "get_all_expenses / get_all_incomes")
    Rel(gen_agent, math_tool, "Executa contas determinísticas", "evaluate")
```

---

## 2. Contratos e Interfaces Técnicas

### 2.1 Modelo de Dados de Contexto e Retorno
```python
@dataclass
class AgentContext:
    message: str
    history: list[dict[str, str]]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResult:
    reply: str
    agent_name: str
    confidence: float
    pending_transaction: Optional[dict] = None
    report_data: Optional[dict] = None
    action_taken: Optional[str] = None
    suggested_actions: list[str] = field(default_factory=list)
```

### 2.2 Contrato Base do Agente Especializado (`BaseAgent`)
```python
class BaseAgent(ABC):
    name: str
    description: str

    @abstractmethod
    def can_handle(self, context: AgentContext) -> float:
        """Retorna uma pontuação de confiança (0.0 a 1.0) sobre a capacidade do agente em resolver o pedido."""
        pass

    @abstractmethod
    def process(self, context: AgentContext) -> AgentResult:
        """Executa a tarefa especializada e retorna o resultado estruturado."""
        pass
```

### 2.3 Registro Dinâmico (`AgentRegistry`)
```python
class AgentRegistry:
    def register(self, agent: BaseAgent) -> None: ...
    def get(self, name: str) -> Optional[BaseAgent]: ...
    def get_all(self) -> list[BaseAgent]: ...
    def find_best_agent(self, context: AgentContext) -> tuple[BaseAgent, float]: ...
```

---

## 3. Critérios de Aceitação e Qualidade

1. **Extensibilidade e Plug-and-Play:**
   - Criar um novo agente deve exigir apenas estender `BaseAgent` e registrá-lo no `AgentRegistry`.
   - Nenhuma modificação nas rotas do FastAPI (`/api/chat`, etc.) deve ser necessária para habilitar um novo agente especializado.
2. **Conformidade com Clean Architecture:**
   - Domínio (`src/guardrail/` e contratos de agente): livre de dependências de framework web ou bibliotecas de UI.
   - Aplicação (`src/agent/`): orquestração pura, controle de histórico e supervisão.
   - Infraestrutura (`src/services/`, `src/tools/`): integrações externas isoladas.
3. **Determinismo Aritmético:**
   - Nenhuma operação matemática em relatórios ou cálculos deve ser inventada por LLM livre; deve ser computada via `MathTool` ou rotinas analíticas do `ReportAgent`.
4. **Resiliência e Fallback Gracioso:**
   - Se um agente especializado falhar ou tempo limite expirar, o `AgentRouter` deve ativar fallback seguro para o `GeneralFinancialAgent` sem derrubar a API.
5. **Compatibilidade com Frontend:**
   - O payload do endpoint `/api/chat` mantém estrita retrocompatibilidade com o frontend Next.js (`reply`, `pending_transaction`, `report_data`), adicionando campos enriquecidos (`agent_name`, `suggested_actions`).
6. **Cobertura de Testes:**
   - 100% dos testes existentes (34 testes unitários) devem continuar passando.
   - Novos testes unitários dedicados para cada agente especializado (`TransactionAgentTest`, `ReportAgentTest`, `AdvisoryAgentTest`, `AgentRegistryTest`, `RouterTest`).
