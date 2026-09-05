# 🛠️ Tutorial: Como Criar e Acoplar Novos Agentes Especialistas

Este tutorial é um guia prático para desenvolvedores que desejam adicionar novos agentes especialistas ao sistema.

A arquitetura adota o **Princípio Aberto/Fechado (SOLID)**: o sistema está **aberto para extensão**, mas **fechado para modificação**.  
Isso significa que você pode criar e plugar novos agentes **sem modificar nenhuma rota da API FastAPI**, sem alterar o frontend Next.js e sem mexer no código dos outros agentes existentes.

---

## 📋 As 4 Etapas de Criação de um Agente

```
1. Definir o Prompt ➔ 2. Criar a Classe (BaseAgent) ➔ 3. Registrar no Router ➔ 4. Escrever o Teste
```

---

### Passo 1: Definir o Prompt do Especialista em `src/agent/prompts.py`

Abra o arquivo [`src/agent/prompts.py`](../src/agent/prompts.py) e adicione a constante com o prompt do seu agente.  
O prompt deve definir claramente a **persona**, o **escopo**, as **ferramentas permitidas** e as **regras de conduta**.

```python
# Em src/agent/prompts.py:

INVESTMENT_AGENT_PROMPT = """Você é o Especialista em Simulação de Investimentos (InvestmentAgent).
Sua missão é ajudar o usuário a simular rendimentos de renda fixa (CDB, Tesouro Direto, LCI/LCA).

RESPONSABILIDADES:
- Calcular simulações de rendimento bruto e líquido com base no prazo informado.
- Alertar sobre alíquotas de Imposto de Renda (tabela regressiva) e IOF.
- Recomendar sempre a constituição de reserva de emergência antes de aportes de risco.

REGRAS DE CONDUTA:
- NUNCA prometa lucros garantidos fora de ativos de renda fixa pós-fixada.
- Cálculos com juros compostos devem utilizar as ferramentas determinísticas.
"""
```

---

### Passo 2: Criar a Classe do Agente em `src/agent/specialists/`

Crie o arquivo do seu agente (por exemplo, `src/agent/specialists/investment_agent.py`):

```python
# src/agent/specialists/investment_agent.py
import re
from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.agent.prompts import INVESTMENT_AGENT_PROMPT
from src.tools.math_tool import MathTool

class InvestmentAgent(BaseAgent):
    """Especialista em projeções de investimentos e renda fixa."""

    def __init__(self):
        super().__init__(
            name="investment_agent",
            description="Especialista em cálculo de rendimento de CDB, Tesouro Direto e projeções financeiras."
        )
        # Associa o prompt especializado criado no Passo 1
        self.system_prompt = INVESTMENT_AGENT_PROMPT

    def can_handle(self, context: AgentContext) -> float:
        """
        Retorna a pontuação de afinidade da mensagem:
        - 0.90 a 1.0: intenção prioritária deste especialista
        - 0.50 a 0.89: intenção parcial
        - abaixo de 0.20: fora do escopo deste especialista
        """
        msg_lower = context.message.lower()
        invest_terms = ["investir", "investimento", "cdb", "tesouro direto", "lci", "lca", "rendimento"]

        if any(term in msg_lower for term in invest_terms):
            return 0.95
        return 0.05

    def process(self, context: AgentContext) -> AgentResult:
        """
        Executa a lógica do especialista e retorna o AgentResult estruturado.
        """
        msg_lower = context.message.lower()

        # Exemplo de extração de valor
        numbers = re.findall(r"\d+", msg_lower)
        valor_investir = float(numbers[0]) if numbers else 1000.0

        # Cálculo determinístico: 100% do CDI estimado em 11.5% ao ano
        rendimento_anual = MathTool.multiply(valor_investir, 0.115)
        total_estimado = MathTool.add(valor_investir, rendimento_anual)

        resposta = (
            f"### 📈 Simulação de Investimento em Renda Fixa (100% do CDI)\n"
            f"- **Aporte Simulado:** R$ {valor_investir:.2f}\n"
            f"- **Rendimento Bruto Estimado (1 ano):** R$ {rendimento_anual:.2f}\n"
            f"- **Total Bruto Projetado:** **R$ {total_estimado:.2f}**\n\n"
            f"*(Estimativa com CDI a 11,50% a.a. Sujeito a incidência de I.R. regressivo no resgate)*"
        )

        return AgentResult(
            reply=resposta,
            agent_name=self.name,
            confidence=0.95,
            suggested_actions=["Ver Saldo Atual", "Cadastrar Despesa", "Dicas de Economia"]
        )
```

Exporte seu agente em [`src/agent/specialists/__init__.py`](../src/agent/specialists/__init__.py):
```python
from src.agent.specialists.investment_agent import InvestmentAgent
```

---

### Passo 3: Registrar o Agente no `AgentRouter`

Basta registrar a instância no `AgentRouter` ou no `AgentRegistry`.  
No arquivo [`src/agent/router.py`](../src/agent/router.py), dentro de `_register_default_specialists`:

```python
from src.agent.specialists.investment_agent import InvestmentAgent

def _register_default_specialists(self) -> None:
    ...
    self.registry.register(InvestmentAgent())
```

> ⚡ **Também funciona via injeção dinâmica:**  
> Se você quiser adicionar um agente temporário ou experimental em tempo de execução sem editar código:
> ```python
> router = AgentRouter()
> router.registry.register(MeuAgenteCustomizado())
> ```

---

### Passo 4: Escrever o Teste Automatizado em `tests/`

Adicione um teste unitário em [`tests/test_specialist_agents.py`](../tests/test_specialist_agents.py):

```python
def test_investment_agent():
    from src.agent.specialists.investment_agent import InvestmentAgent
    agent = InvestmentAgent()

    # 1. Valida detecção de intenção
    assert agent.can_handle(AgentContext(message="quero investir 5000 no cdb")) >= 0.90
    assert agent.can_handle(AgentContext(message="qual o meu saldo?")) <= 0.20

    # 2. Valida processamento e resposta
    res = agent.process(AgentContext(message="quero investir 5000 no cdb"))
    assert res.agent_name == "investment_agent"
    assert "Simulação de Investimento" in res.reply
    assert "5000.00" in res.reply
```

Execute os testes com `uv run pytest`:
```bash
uv run pytest tests/test_specialist_agents.py
```

---

## 🎯 Contrato `AgentResult`: O que o agente pode retornar?

O objeto `AgentResult` suporta os seguintes campos estruturados:

| Campo | Tipo | Descrição |
|---|---|---|
| `reply` | `str` (Obrigatório) | O texto de resposta final em Markdown formatado para o usuário. |
| `agent_name` | `str` (Obrigatório) | Identificador do especialista (ex: `"investment_agent"`). |
| `confidence` | `float` | Nível de confiança da resposta (0.0 a 1.0). |
| `pending_transaction` | `Optional[dict]` | Se o agente quiser acionar o card de confirmação com botões no frontend. |
| `report_data` | `Optional[dict]` | Se o agente quiser renderizar gráficos de barras no painel visual. |
| `suggested_actions` | `list[str]` | Lista de chips/botões com sugestões de mensagens rápidas. |
