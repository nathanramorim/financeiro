# 🧭 Guia do Assistente Financeiro para Leigos

Bem-vindo! Este documento foi escrito para que qualquer pessoa — mesmo sem conhecimento de programação — entenda exatamente como o nosso assistente financeiro funciona, quem são os "agentes especialistas" e como tirar o melhor proveito de cada um no chat.

---

## 🏢 O que é uma Arquitetura Multiagente?

Imagine um escritório financeiro tradicional: se você tiver apenas uma pessoa para atender o telefone, fazer a contabilidade, montar gráficos complexos, dar consultoria de investimentos e auditar notas fiscais, ela ficará sobrecarregada e cometerá erros.

Uma **Arquitetura Multiagente** funciona como uma **equipe de especialistas**:
- Há um **Recepcionista Inteligente (Supervisor/Roteador)** que ouve a sua mensagem.
- Ele identifica imediatamente qual especialista da equipe é o mais competente para resolver o seu pedido.
- O especialista entra em ação, realiza o trabalho com precisão cirúrgica e devolve a resposta pronta para você.

---

## 📝 O que é o "Prompt" de cada Agente?

O **Prompt** é a "descrição de cargo" e o conjunto de regras de conduta do agente. 
É nele que definimos:
- **Quem ele é** (sua personalidade e tom de voz).
- **O que ele pode e não pode fazer** (por exemplo: nunca inventar números de cabeça).
- **Como ele deve responder** (formatação, clareza, empatia).

> 📍 **Onde ficam os prompts no projeto?**  
> Todos os prompts dos especialistas estão centralizados e organizados no arquivo:  
> [`backend/agent/prompts.py`](../backend/agent/prompts.py)

---

## 👥 Conheça a sua Equipe de Agentes Especialistas

Abaixo estão os especialistas que trabalham para você todos os dias:

### 1. 💳 O Registrador (`TransactionAgent`)
- **Quem é:** É o auditor contábil da equipe. Ele não perde um centavo e cuida de registrar tudo o que entra e sai do seu bolso.
- **O que ele faz:** Identifica se você gastou ou ganhou dinheiro, descobre a categoria (ex: Alimentação, Transporte, Moradia) e prepara um cartão para você confirmar a operação com um clique antes de gravar na planilha.
- **Frases de exemplo para falar no chat:**
  - *"Gastei R$ 45 no almoço"*
  - *"Adicionei despesa Mercado R$ 250"*
  - *"Recebi R$ 1200 de um freela"*
  - *"Comprei remédio na farmácia por 85 reais"*

---

### 2. 📊 O Analista de Relatórios (`ReportAgent`)
- **Quem é:** É o analista de dados executivo. Ele consolida seus lançamentos e gera panoramas claros e visuais da sua vida financeira.
- **O que ele faz:** Soma receitas, calcula total de despesas, apura o saldo líquido, agrupa os gastos por categoria e envia os dados diretamente para os gráficos do painel.
- **Frases de exemplo para falar no chat:**
  - *"Gerar relatório financeiro"*
  - *"Qual o meu saldo atual?"*
  - *"Exibir gráficos de despesas"*
  - *"Quanto sobrou este mês?"*

---

### 3. 💡 O Consultor Pessoal (`AdvisoryAgent`)
- **Quem é:** É o seu educador e planejador financeiro pessoal. Ele não apenas olha os números, mas orienta sobre o que fazer com eles.
- **O que ele faz:** Avalia se você está no vermelho ou no azul, identifica qual categoria está "comendo" mais o seu orçamento e ensina a aplicar a famosa **Regra 50/30/20** (50% para necessidades, 30% para estilo de vida, 20% para poupança).
- **Frases de exemplo para falar no chat:**
  - *"Como posso economizar dinheiro este mês?"*
  - *"Estou gastando muito?"*
  - *"Me dê uma dica de planejamento orçamentário"*
  - *"Como aplicar a regra 50/30/20 no meu caso?"*

---

### 4. 🎯 O Guardião de Metas (`BudgetGoalAgent`)
- **Quem é:** O treinador focado nos seus objetivos de poupança (ex: comprar um carro, fazer uma viagem, reserva de emergência).
- **O que ele faz:** Compara o quanto você tem guardado com o valor que você quer alcançar, calcula o percentual atingido e diz quantos reais faltam para você comemorar a vitória.
- **Frases de exemplo para falar no chat:**
  - *"Minha meta é poupar R$ 1000 este mês"*
  - *"Quero guardar R$ 5000 para a reserva de emergência"*
  - *"Como está o progresso da minha meta?"*

---

### 5. 🧠 O Assistente Educacional & Matemático (`GeneralFinancialAgent`)
- **Quem é:** O professor e calculista da equipe.
- **O que ele faz:** Explica termos econômicos complicados (o que é Selic, CDI, inflação) e realiza contas exatas (divisões de contas entre amigos, rateios, multiplicações) utilizando ferramentas matemáticas que nunca erram contas.
- **Frases de exemplo para falar no chat:**
  - *"Divida por 2 minhas despesas fixas"*
  - *"O que é taxa CDI e como ela afeta meu dinheiro?"*
  - *"O que significa ter uma reserva de emergência?"*

---

### 🛡️ O Segurança Invisível (Guardrail)
Antes de qualquer mensagem chegar aos especialistas, ela passa pelo **Guardrail**.  
Se você perguntar algo totalmente fora de finanças (como *"qual a receita de bolo de cenoura?"* ou *"quem ganhou o jogo de futebol ontem?"*), o segurança educadamente avisa que o assistente é exclusivo para finanças pessoais. Isso protege o sistema e economiza processamento.

---

## 📌 Tabela de Consulta Rápida: O que você quer fazer?

| Se o seu objetivo for... | Envie uma mensagem como... | Quem vai te responder? |
|---|---|---|
| Registrar um gasto rápido | *"Add despesa Mercado 180"* | **TransactionAgent** |
| Registrar um salário ou freela | *"Recebi 3500 de salário"* | **TransactionAgent** |
| Ver gráficos e extrato | *"Relatório"* ou *"Gráficos"* | **ReportAgent** |
| Consultar quanto tem de saldo | *"Qual o meu saldo?"* | **ReportAgent** |
| Receber dicas para sobrar dinheiro | *"Como economizar?"* | **AdvisoryAgent** |
| Definir uma meta de economia | *"Minha meta é juntar R$ 2000"* | **BudgetGoalAgent** |
| Dividir despesas com parceiro(a) | *"Divida por 2 minhas despesas fixas"* | **GeneralFinancialAgent** |
| Tirar uma dúvida de investimento | *"O que é taxa Selic?"* | **GeneralFinancialAgent** |
