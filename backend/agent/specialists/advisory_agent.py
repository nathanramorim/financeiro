from typing import Optional
from backend.agent.base import BaseAgent, AgentContext, AgentResult
from backend.agent.prompts import ADVISORY_AGENT_PROMPT
from backend.tools.expenses import ExpenseTool
from backend.tools.income import IncomeTool
from backend.tools.math_tool import MathTool

class AdvisoryAgent(BaseAgent):
    """Especialista em consultoria financeira pessoal, boas práticas orçamentárias e dicas de economia."""

    def __init__(self, expense_tool: Optional[ExpenseTool] = None, income_tool: Optional[IncomeTool] = None):
        super().__init__(
            name="advisory_agent",
            description="Especialista em diagnóstico financeiro, regra 50/30/20, metas de economia e orientação orçamentária."
        )
        self.system_prompt = ADVISORY_AGENT_PROMPT
        self.expense_tool = expense_tool or ExpenseTool()
        self.income_tool = income_tool or IncomeTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        advisory_keywords = [
            "como economizar", "economizar", "dica", "dicas", "conselho",
            "conselhos", "orçamento", "orcamento", "gasto muito", "gastando muito",
            "cortar gastos", "planejamento financeiro", "meta de economia", "regra 50/30/20"
        ]
        if any(kw in msg_lower for kw in advisory_keywords):
            return 0.94

        return 0.15

    def process(self, context: AgentContext) -> AgentResult:
        expenses = self.expense_tool.list_all_expenses()
        incomes = self.income_tool.service.get_incomes()

        tot_despesas = sum(MathTool.parse_float(e.get("Valor", 0)) for e in expenses)
        tot_receitas = sum(MathTool.parse_float(i.get("Valor", 0)) for i in incomes)
        saldo = tot_receitas - tot_despesas

        # Análise por categoria para identificar o maior ofensor
        cat_dict = {}
        for e in expenses:
            cat = e.get("Categoria") or "Outros"
            val = MathTool.parse_float(e.get("Valor", 0))
            cat_dict[cat] = cat_dict.get(cat, 0.0) + val

        top_cat = max(cat_dict.items(), key=lambda x: x[1])[0] if cat_dict else "Geral"
        top_val = cat_dict.get(top_cat, 0.0)

        lines = [
            "### 💡 Diagnóstico e Consultoria Financeira",
            f"- **Receitas Atuais:** R$ {tot_receitas:.2f}",
            f"- **Despesas Atuais:** R$ {tot_despesas:.2f}",
            f"- **Saldo Disponível:** R$ {saldo:.2f}\n"
        ]

        if saldo < 0:
            lines.append("⚠️ **Alerta de Déficit Orçamentário:**")
            lines.append(f"Suas despesas superam suas receitas em **R$ {abs(saldo):.2f}**.")
            lines.append(f"Seu maior centro de custo é **{top_cat}** (R$ {top_val:.2f}). Recomenda-se renegociação imediata ou redução preventiva nesta categoria.\n")
        else:
            lines.append("✅ **Superávit Identificado:**")
            lines.append(f"Você possui **R$ {saldo:.2f}** livres para direcionar à sua reserva de emergência ou investimentos.\n")

        lines.append("#### 📐 Regra Recomendada 50 / 30 / 20:")
        if tot_receitas > 0:
            necessidades = tot_receitas * 0.50
            desejos = tot_receitas * 0.30
            poupanca = tot_receitas * 0.20
            lines.append(f"- **50% Necessidades Essenciais:** até R$ {necessidades:.2f}")
            lines.append(f"- **30% Estilo de Vida e Desejos:** até R$ {desejos:.2f}")
            lines.append(f"- **20% Reserva e Investimentos:** ideal R$ {poupanca:.2f}")
        else:
            lines.append("- **50%** para custos fixos essenciais (moradia, alimentação, saúde).")
            lines.append("- **30%** para despesas flexíveis (lazer, compras).")
            lines.append("- **20%** para quitação de dívidas ou formação de reserva financeira.")

        lines.append("\n*Quer simular um plano para alcançar uma meta de economia este mês?*")

        return AgentResult(
            reply="\n".join(lines),
            agent_name=self.name,
            confidence=0.94,
            suggested_actions=["Ver Relatório", "Cadastrar Despesa", "Saldo Atual"]
        )
