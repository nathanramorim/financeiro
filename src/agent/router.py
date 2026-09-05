import logging
from typing import Optional
from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.agent.registry import AgentRegistry
from src.agent.specialists.transaction_agent import TransactionAgent
from src.agent.specialists.report_agent import ReportAgent
from src.agent.specialists.advisory_agent import AdvisoryAgent
from src.agent.specialists.general_agent import GeneralFinancialAgent
from src.tools.expenses import ExpenseTool
from src.tools.income import IncomeTool

logger = logging.getLogger("AgentRouter")

class AgentRouter:
    """
    Supervisor / Roteador Multiagente.
    Avalia a mensagem e contexto, seleciona o agente especialista mais qualificado
    no AgentRegistry e delega a execução com fallback resiliente.
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        expense_tool: Optional[ExpenseTool] = None,
        income_tool: Optional[IncomeTool] = None,
    ):
        self.expense_tool = expense_tool or ExpenseTool()
        self.income_tool = income_tool or IncomeTool()

        if registry:
            self.registry = registry
        else:
            self.registry = AgentRegistry()
            self._register_default_specialists()

    def _register_default_specialists(self) -> None:
        """Registra a malha padrão de especialistas financeiros."""
        self.registry.register(TransactionAgent(expense_tool=self.expense_tool, income_tool=self.income_tool))
        self.registry.register(ReportAgent(expense_tool=self.expense_tool, income_tool=self.income_tool))
        self.registry.register(AdvisoryAgent(expense_tool=self.expense_tool, income_tool=self.income_tool))
        self.registry.register(GeneralFinancialAgent(expense_tool=self.expense_tool))

    def route(self, context: AgentContext) -> AgentResult:
        """
        Roteia o contexto para o melhor agente especialista disponível.
        Em caso de erro na execução do especialista, aciona fallback resiliente
        para o GeneralFinancialAgent.
        """
        best_agent, score = self.registry.find_best_agent(context)

        # Se nenhum agente atingir afinidade mínima, usa o general_agent
        if not best_agent or score < 0.25:
            best_agent = self.registry.get("general_agent") or GeneralFinancialAgent(expense_tool=self.expense_tool)

        try:
            result = best_agent.process(context)
            # Garante que o nome do agente executor esteja preenchido
            if not result.agent_name:
                result.agent_name = best_agent.name
            return result
        except Exception as e:
            logger.error(f"Falha ao executar especialista {best_agent.name}: {e}. Ativando fallback.", exc_info=True)
            fallback_agent = self.registry.get("general_agent")
            if fallback_agent and fallback_agent != best_agent:
                try:
                    fallback_res = fallback_agent.process(context)
                    fallback_res.reply += f"\n\n*(Nota: processado via agente de contingência devido a instabilidade técnica)*"
                    return fallback_res
                except Exception as fb_err:
                    logger.critical(f"Falha no fallback: {fb_err}")

            return AgentResult(
                reply="⚠️ Ocorreu uma instabilidade ao processar sua solicitação financeira. Por favor, tente novamente.",
                agent_name="system_fallback",
                confidence=0.0
            )

    # Métodos de conveniência e retrocompatibilidade com a API / testes legados:

    def process_message(self, user_message: str, history: list[dict] = None) -> str:
        ctx = AgentContext(message=user_message, history=history or [])
        res = self.route(ctx)
        return res.reply

    def detect_mutation_intent(self, user_message: str) -> Optional[dict]:
        tx_agent = self.registry.get("transaction_agent")
        if isinstance(tx_agent, TransactionAgent):
            return tx_agent.detect_mutation_intent(user_message)
        return TransactionAgent(self.expense_tool, self.income_tool).detect_mutation_intent(user_message)

    def is_report_request(self, user_message: str) -> bool:
        rep_agent = self.registry.get("report_agent")
        if rep_agent:
            return rep_agent.can_handle(AgentContext(message=user_message)) >= 0.90
        return any(term in user_message.lower() for term in ["relatorio", "relatório", "grafico", "gráfico", "gráficos", "graficos"])

    def generate_report_data(self) -> dict:
        rep_agent = self.registry.get("report_agent")
        if isinstance(rep_agent, ReportAgent):
            return rep_agent.generate_report_data()
        return ReportAgent(self.expense_tool, self.income_tool).generate_report_data()

    def execute_transaction(self, tx: dict) -> str:
        tx_agent = self.registry.get("transaction_agent")
        if isinstance(tx_agent, TransactionAgent):
            return tx_agent.execute_transaction(tx)
        return TransactionAgent(self.expense_tool, self.income_tool).execute_transaction(tx)
