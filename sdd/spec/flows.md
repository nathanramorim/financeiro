# Fluxos — financeiro

## 1. Fluxo Principal de Processamento de Mensagens

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário
    participant UI as Web UI (Streamlit)
    participant Guardrail as Guardrail Module
    participant Agent as Agente Financeiro (OpenRouter)
    participant Math as MathTool
    participant Sheets as Google Sheets Service

    User->>UI: Envia pergunta/comando no chat
    UI->>Guardrail: Valida mensagem de entrada
    alt Mensagem Inválida / Fora de Escopo
        Guardrail-->>UI: Retorna aviso de recusa por escopo
        UI-->>User: Exibe mensagem de bloqueio amigável
    else Mensagem Válida
        Guardrail->>Agent: Encaminha mensagem validada
        Agent->>Agent: Analisa intenção e decide Tool
        opt Requer Cálculo (ex: dividir despesas por 2)
            Agent->>Math: Executa cálculo numérico
            Math-->>Agent: Retorna valor exato
        end
        opt Requer Leitura / Escrita em Planilha
            Agent->>Sheets: Consulta ou Grava (Despesas/Receitas)
            Sheets-->>Agent: Retorna dados atualizados / confirmação
        end
        Agent-->>UI: Resposta final estruturada
        UI-->>User: Exibe resposta no chat
    end
```

## 2. Fluxo de Consulta de Despesas Fixas e Saldo
1. Usuário solicita: *"Qual o total das minhas despesas fixas este mês e meu saldo?"*
2. Guardrail aprova a solicitação.
3. Agente ativa a Tool de Despesas e busca na planilha as linhas classificadas como `fixa`.
4. Agente ativa a Tool de Saldo para obter total de receitas vs despesas.
5. Agente formata os dados e retorna o resumo para a UI.

## 3. Fluxo de Cadastro com Operação Matemática e Categorização
1. Usuário solicita: *"Cadastre a despesa de Aluguel de R$ 1500 multiplicada por 2 e categorize"*.
2. Guardrail valida e aprova.
3. Agente executa `MathTool.evaluate("1500 * 2")` -> `R$ 3000`.
4. Agente chama `CategoryModule` -> categoriza como `Moradia / Despesa Fixa`.
5. Agente chama `SheetsService` -> insere nova linha na planilha Google Sheets.
6. Agente confirma o cadastro na interface de chat.
