from typing import Optional
from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.agent.prompts import REPORT_AGENT_PROMPT
from src.tools.expenses import ExpenseTool
from src.tools.income import IncomeTool
from src.tools.category import CategoryTool
from src.tools.math_tool import MathTool

class ReportAgent(BaseAgent):
    """Especialista em geração de relatórios executivos, saldos e agregações por categoria."""

    def __init__(self, expense_tool: Optional[ExpenseTool] = None, income_tool: Optional[IncomeTool] = None):
        super().__init__(
            name="report_agent",
            description="Especialista em consolidação analítica, saldos líquidos, relatórios e métricas de categorias."
        )
        self.system_prompt = REPORT_AGENT_PROMPT
        self.expense_tool = expense_tool or ExpenseTool()
        self.income_tool = income_tool or IncomeTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        if any(term in msg_lower for term in ["relatorio", "relatório", "grafico", "gráfico", "gráficos", "graficos", "extrato", "resumo executivo", "resumo financeiro"]):
            return 0.98

        if any(term in msg_lower for term in ["saldo", "balanço", "balanco", "quanto gastei", "quanto sobrou"]):
            return 0.90

        if "despesas fixas" in msg_lower or "listar despesas" in msg_lower:
            return 0.85

        return 0.10

    def generate_report_data(self) -> dict:
        expenses = self.expense_tool.list_all_expenses()
        incomes = self.income_tool.service.get_incomes()

        tot_despesas = sum(MathTool.parse_float(e.get("Valor", 0)) for e in expenses)
        tot_receitas = sum(MathTool.parse_float(i.get("Valor", 0)) for i in incomes)
        saldo = tot_receitas - tot_despesas

        cat_dict = {}
        for e in expenses:
            cat = e.get("Categoria")
            if not cat or str(cat).strip().lower() in ["", "outros", "none", "geral"]:
                inferred = CategoryTool.categorize(e.get("Descrição", ""))
                cat = inferred if inferred else "Outros"
            val = MathTool.parse_float(e.get("Valor", 0))
            cat_dict[cat] = cat_dict.get(cat, 0.0) + val

        return {
            "total_receitas": round(tot_receitas, 2),
            "total_despesas": round(tot_despesas, 2),
            "saldo_liquido": round(saldo, 2),
            "despesas_por_categoria": {k: round(v, 2) for k, v in cat_dict.items()}
        }

    def process(self, context: AgentContext) -> AgentResult:
        msg_lower = context.message.lower()

        # 1. Apenas saldo / balanço rápido
        if ("saldo" in msg_lower or "balanço" in msg_lower or "balanco" in msg_lower) and not any(term in msg_lower for term in ["relatorio", "relatório", "grafico", "gráfico"]):
            bal = self.income_tool.get_balance()
            reply = (
                f"### 💰 Resumo do Saldo Atual\n"
                f"- **Total de Receitas:** R$ {bal['total_receitas']:.2f}\n"
                f"- **Total de Despesas:** R$ {bal['total_despesas']:.2f}\n"
                f"- **Saldo Líquido:** **R$ {bal['saldo_liquido']:.2f}**"
            )
            return AgentResult(
                reply=reply,
                agent_name=self.name,
                confidence=0.95,
                suggested_actions=["Ver Relatório Completo", "Cadastrar Despesa"]
            )

        # 2. Listar apenas despesas fixas
        if ("despesas fixas" in msg_lower or "listar despesas" in msg_lower) and not any(term in msg_lower for term in ["relatorio", "relatório", "grafico", "gráfico"]):
            expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 📋 Despesas Fixas Cadastradas:"]
            for exp in expenses:
                res.append(f"- **{exp['Descrição']}** ({exp['Categoria']}): R$ {MathTool.parse_float(exp['Valor']):.2f}")
            return AgentResult(
                reply="\n".join(res),
                agent_name=self.name,
                confidence=0.90,
                suggested_actions=["Ver Relatório Executivo", "Saldo Atual"]
            )

        # 3. Relatório completo com dados analíticos de categoria
        report = self.generate_report_data()
        lines = [
            "### 📊 Relatório Financeiro Executivo",
            f"- **Total de Receitas:** R$ {report['total_receitas']:.2f}",
            f"- **Total de Despesas:** R$ {report['total_despesas']:.2f}",
            f"- **Saldo Líquido:** **R$ {report['saldo_liquido']:.2f}**\n",
            "#### 🏷️ Despesas por Categoria:"
        ]
        for cat, val in report["despesas_por_categoria"].items():
            lines.append(f"- **{cat}:** R$ {val:.2f}")
        lines.append("\n*Gráficos gerados e renderizados na interface abaixo.*")

        return AgentResult(
            reply="\n".join(lines),
            agent_name=self.name,
            confidence=0.98,
            report_data=report,
            suggested_actions=["Cadastrar Despesa", "Dicas de Economia", "Saldo Atual"]
        )
