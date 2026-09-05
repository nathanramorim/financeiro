import re
from typing import Optional
from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.agent.prompts import BUDGET_GOAL_AGENT_PROMPT
from src.tools.income import IncomeTool
from src.tools.expenses import ExpenseTool
from src.tools.math_tool import MathTool

class BudgetGoalAgent(BaseAgent):
    """
    Agente especialista de extensão: Gerencia metas de economia e tetos orçamentários.
    Demonstra a facilidade de criar e acoplar novos agentes via plug-and-play sem tocar na API.
    """

    def __init__(self, income_tool: Optional[IncomeTool] = None, expense_tool: Optional[ExpenseTool] = None):
        super().__init__(
            name="budget_goal_agent",
            description="Especialista em definição de metas de economia, tetos orçamentários e acompanhamento de poupança."
        )
        self.system_prompt = BUDGET_GOAL_AGENT_PROMPT
        self.income_tool = income_tool or IncomeTool()
        self.expense_tool = expense_tool or ExpenseTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        # Gatilhos de metas orçamentárias
        goal_keywords = ["meta", "metas", "teto orçamentário", "poupar", "guardar dinheiro", "reserva"]
        if any(kw in msg_lower for kw in goal_keywords):
            return 0.96

        return 0.10

    def process(self, context: AgentContext) -> AgentResult:
        msg_lower = context.message.lower()
        bal = self.income_tool.get_balance()
        saldo = bal["saldo_liquido"]

        # Busca valores numéricos mencionados na mensagem como meta
        numbers = re.findall(r"r\$\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)", msg_lower)
        target_val = 0.0
        for n in numbers:
            val_str = n[0] or n[1]
            if val_str:
                v = MathTool.parse_float(val_str)
                if v > 0:
                    target_val = v
                    break

        lines = ["### 🎯 Acompanhamento de Metas Financeiras"]

        if target_val > 0:
            lines.append(f"- **Meta Informada:** R$ {target_val:.2f}")
            lines.append(f"- **Saldo Líquido Atual:** R$ {saldo:.2f}")

            if saldo >= target_val:
                lines.append("🎉 **Parabéns! Sua meta já foi atingida com base no saldo disponível!**")
                lines.append(f"Você superou a meta em **R$ {saldo - target_val:.2f}**.")
            elif saldo > 0:
                percent = (saldo / target_val) * 100
                restante = target_val - saldo
                lines.append(f"- **Progresso Atual:** {percent:.1f}% alcançado.")
                lines.append(f"- **Faltam apenas:** R$ {restante:.2f} para bater seu objetivo.")
            else:
                lines.append(f"⚠️ Atualmente seu saldo está negativo (R$ {saldo:.2f}). Foque em reduzir despesas essenciais antes de constituir novos aportes.")
        else:
            lines.append("- **Saldo Disponível para Metas:** R$ {:.2f}".format(saldo))
            lines.append("Para definir uma meta de poupança, mencione o valor desejado (ex: *Quero atingir a meta de R$ 1000 este mês*).")

        return AgentResult(
            reply="\n".join(lines),
            agent_name=self.name,
            confidence=0.96,
            suggested_actions=["Ver Relatório", "Dicas de Economia", "Saldo Atual"]
        )
