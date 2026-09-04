# Discovery 01 — Agente Financeiro Inteligente com Web Chat e Google Sheets

## 1. Visão de Produto (O "Porquê")
Usuários de finanças pessoais frequentemente enfrentam dificuldades para manter suas planilhas organizadas manualmente ou dependem de interfaces complexas. Este projeto busca resolver esse problema através de uma interface de Web Chat conversacional orientada a linguagem natural, permitindo consultar despesas fixas, cadastrar novos gastos/receitas, visualizar o saldo acumulado, categorizar despesas e realizar ajustes/cálculos numéricos (ex: dividir despesas por 2 ou aplicar multiplicadores) de forma simples e segura.

## 2. Público-Alvo e Casos de Uso (O "Para Quem")
- **Público:** Pessoas físicas que desejam gerenciar suas despesas fixas e orçamento pessoal via conversa sem abrir planilhas complexas.
- **Casos de Uso Principais:**
  - *Consulta de Despesas Fixas:* "Quais são minhas despesas fixas cadastradas este mês?"
  - *Cadastro de Despesa com Operação:* "Cadastre o valor da conta de internet de R$ 100 multiplicada por 2."
  - *Divisão / Ajuste em Despesas:* "Divida por 2 o valor da despesa de aluguel."
  - *Gestão de Receitas e Saldo:* "Qual o meu saldo atual considerando minhas receitas e despesas?"
  - *Categorização Automática:* "Atribua a categoria Moradia para o condomínio."

## 3. Escopo Funcional (O "Como" Macro)
- **Web Chat UI:** Interface gráfica limpa para interação conversacional com mensagens de usuário e respostas do assistente.
- **Integração OpenRouter:** Conexão com modelos de linguagem avançados para interpretação de intenções e chamadas de ferramentas.
- **Camada de Guardrail:** Interceptação de mensagens para bloquear tentativas de fora de escopo (ex: perguntas sobre código, política, culinária) ou ataques de segurança/jailbreak.
- **Integração Google Sheets:** Persistência dos registros de despesas fixas, variáveis, receitas e saldo em planilha no Google Sheets via OAuth2 ou Service Account (`gspread`).
- **Engine Matemático (MathTool):** Módulo Python seguro para realizar operações aritméticas (multiplicação, divisão por N) sem depender de alucinações numéricas da LLM.
- **Categorizador de Gastos:** Classificação de despesas em categorias padrão (Moradia, Alimentação, Transporte, Saúde, Lazer).
