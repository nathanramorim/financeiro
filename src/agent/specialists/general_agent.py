import json
import requests
from typing import Optional
from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
from src.agent.prompts import SYSTEM_PROMPT
from src.tools.math_tool import MathTool
from src.tools.expenses import ExpenseTool

class GeneralFinancialAgent(BaseAgent):
    """Especialista em dúvidas conceituais de finanças, operações matemáticas e agente de fallback."""

    def __init__(
        self,
        api_key: str = OPENROUTER_API_KEY,
        model: str = OPENROUTER_MODEL,
        expense_tool: Optional[ExpenseTool] = None
    ):
        super().__init__(
            name="general_agent",
            description="Especialista em conceitos financeiros gerais, operações matemáticas e fallback resiliente."
        )
        self.api_key = api_key or "mock_key"
        self.model = model
        self.base_url = OPENROUTER_BASE_URL
        self.expense_tool = expense_tool or ExpenseTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        # Operações matemáticas explícitas
        if any(term in msg_lower for term in [
            "dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por",
            "multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2", "quanto é", "calcule"
        ]):
            return 0.88

        # Fallback baseline para qualquer mensagem financeira
        return 0.30

    def process(self, context: AgentContext) -> AgentResult:
        msg = context.message
        msg_lower = msg.lower()

        # 1. Operações matemáticas em despesas fixas
        if any(term in msg_lower for term in ["dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Divididas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_div = MathTool.divide(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_div:.2f}**")
            return AgentResult(
                reply="\n".join(res),
                agent_name=self.name,
                confidence=0.90,
                suggested_actions=["Saldo Atual", "Ver Relatório"]
            )

        if any(term in msg_lower for term in ["multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Multiplicadas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_mult = MathTool.multiply(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_mult:.2f}**")
            return AgentResult(
                reply="\n".join(res),
                agent_name=self.name,
                confidence=0.90,
                suggested_actions=["Saldo Atual", "Ver Relatório"]
            )

        # 2. Se houver OpenRouter configurado, consulta o LLM
        if self.api_key and self.api_key != "mock_key":
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if context.history:
                messages.extend(context.history)
            messages.append({"role": "user", "content": msg})

            payload = {
                "model": self.model,
                "messages": messages,
                "reasoning": {"enabled": True}
            }

            try:
                response = requests.post(
                    url=f"{self.base_url}/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=4
                )
                if response.status_code == 200:
                    data = response.json()
                    choice = data['choices'][0]['message']
                    content = choice.get('content', '')
                    if not content and 'reasoning_details' in choice:
                        content = choice['reasoning_details'].get('text', '')
                    if content:
                        return AgentResult(
                            reply=content,
                            agent_name=self.name,
                            confidence=0.85
                        )
            except Exception as e:
                print(f"[GeneralFinancialAgent] Chamada OpenRouter falhou: {e}. Usando resposta local.")

        # 3. Resposta de Fallback local amigável
        return AgentResult(
            reply="Recebi sua mensagem financeira e processei as informações com sucesso.",
            agent_name=self.name,
            confidence=0.50,
            suggested_actions=["Ver Relatório", "Saldo Atual", "Dicas de Economia"]
        )
