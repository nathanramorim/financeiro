# Overview — financeiro

O **financeiro** é uma aplicação de assistente virtual para gestão financeira pessoal, com arquitetura desacoplada: backend em FastAPI e frontend Web Chat em Next.js (App Router). O sistema processa solicitações em linguagem natural via modelos LLM (conectados via OpenRouter) roteadas para agentes especialistas, aplica uma camada estrita de guardrails para garantir foco e segurança no domínio financeiro, executa operações matemáticas com precisão através de ferramentas dedicadas e persiste receitas e despesas no Google Sheets com cache resiliente.

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
  subgraph Frontend["Frontend Next.js (:3020)"]
    WebUI["💻 Interface Web Chat<br/>(App Router, Tailwind)"]
  end

  subgraph Backend["Backend FastAPI (:8000)"]
    API["🌐 API REST<br/>(/api/chat, /api/transactions, /api/reports)"]
    Guardrail["🛡️ Camada de Guardrail<br/>(Validador de Escopo & Segurança)"]
    Router["🧭 Router / Supervisor<br/>(Malha Multiagente com fallback)"]

    subgraph Specialists["Agentes Especialistas"]
      TransactionAgent["💸 Transaction Agent"]
      ReportAgent["📈 Report Agent"]
      AdvisoryAgent["💡 Advisory Agent"]
      BudgetGoalAgent["🎯 Budget Goal Agent"]
      GeneralAgent["🤖 General Agent"]
    end

    subgraph Tools["Ferramentas"]
      MathTool["🧮 MathTool<br/>(Operações Matemáticas Seguras)"]
      CategoryTool["🏷️ Category Tool<br/>(Classificador de Gastos)"]
    end

    SheetsRepo["🔌 SheetsService<br/>(gspread, cache TTL 30s, backup local)"]
  end

  OpenRouter["☁️ OpenRouter API"]
  GoogleSheets["📊 Google Sheets API"]

  User(("👤 Usuário")) -->|HTTP| WebUI
  WebUI -->|"1. Envia mensagem"| API
  API --> Guardrail
  Guardrail -.->|"Rejeita se fora do escopo"| API
  Guardrail -->|"2. Repassa prompt validado"| Router

  Router -->|"3. Roteia por intenção"| Specialists
  Specialists -->|"Prompt / Function Calling"| OpenRouter
  Specialists --> Tools
  Specialists --> SheetsRepo
  SheetsRepo -->|"OAuth2 / API Call"| GoogleSheets
```
