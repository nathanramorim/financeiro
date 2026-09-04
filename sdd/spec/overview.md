# Overview — financeiro

O **financeiro** é uma aplicação de assistente virtual para gestão financeira pessoal com interface Web Chat. O sistema processa solicitações em linguagem natural via modelos LLM (conectados via OpenRouter), aplica uma camada estrita de guardrails para garantir foco e segurança no domínio financeiro, executa operações matemáticas com precisão através de ferramentas dedicadas e persiste receitas e despesas no Google Sheets.

## Índice
- `stack.md` — tecnologias e estrutura de diretórios
- `modules.md` — componentes e responsabilidades
- `flows.md` — fluxos de execução principais
- `decisions.md` — decisões de arquitetura (ADRs)

---

## Arquitetura (C4 Model)

### Nível 1: Contexto
```mermaid
graph TB
  User(("👤 Usuário"))
  System["🟢 Sistema Financeiro IA<br/>(Interface Web Chat + Agente)"]
  OpenRouter["☁️ OpenRouter API<br/>(LLMs - Claude, GPT, Llama)"]
  GoogleSheets["📊 Google Sheets API<br/>(Planilha de Finanças)"]

  User -->|"Envia mensagens e comandos de finanças"| System
  System -->|"Envia prompts validados & recebe tool calls"| OpenRouter
  System -->|"Lê e grava receitas, despesas e saldos"| GoogleSheets
```

### Nível 2: Containers
```mermaid
graph TB
  subgraph System["Sistema Financeiro IA"]
    WebUI["💻 Interface Web Chat<br/>(Streamlit)"]
    Guardrail["🛡️ Camada de Guardrail<br/>(Validador de Escopo & Segurança)"]
    FinancialAgent["🤖 Agente Financeiro Core<br/>(Orquestrador & LLM OpenRouter Client)"]
    
    subgraph Tools["Ferramentas & Módulos"]
      ExpenseModule["💸 Módulo de Despesas<br/>(Consulta Fixas/Variáveis & Cadastro)"]
      IncomeModule["💰 Módulo de Receitas & Saldo<br/>(Gestão de Entradas e Balanço)"]
      CategoryModule["🏷️ Categorizador de Gastos<br/>(Regras + Classificador)"]
      MathTool["🧮 Calculadora On-Demand<br/>(Operações Matemáticas Seguras)"]
    end
    
    SheetsRepo["🔌 Repositório Google Sheets<br/>(gspread / MCP Google Sheets)"]
  end

  OpenRouter["☁️ OpenRouter API"]
  GoogleSheets["📊 Google Sheets API"]

  User(("👤 Usuário")) -->|HTTP / WebSockets| WebUI
  WebUI -->|"1. Envia mensagem bruta"| Guardrail
  Guardrail -->|"2. Mensagem validada (Financeira)"| Guardrail
  Guardrail -.->|"Rejeita se fora do escopo"| WebUI
  Guardrail -->|"Repassa prompt limpo"| FinancialAgent

  FinancialAgent -->|"3. Prompt / Function Calling"| OpenRouter
  FinancialAgent -->|"4. Executa Tools"| Tools
  
  Tools --> SheetsRepo
  SheetsRepo -->|"OAuth2 / API Call"| GoogleSheets
```
