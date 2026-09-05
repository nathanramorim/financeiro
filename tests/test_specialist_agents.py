import pytest
from unittest.mock import MagicMock
from src.agent.base import AgentContext
from src.agent.specialists.transaction_agent import TransactionAgent
from src.agent.specialists.report_agent import ReportAgent
from src.agent.specialists.advisory_agent import AdvisoryAgent
from src.agent.specialists.general_agent import GeneralFinancialAgent

@pytest.fixture
def mock_expense_tool():
    tool = MagicMock()
    tool.list_all_expenses.return_value = [
        {"Descrição": "Aluguel", "Valor": 1500.0, "Tipo": "fixa", "Categoria": "Moradia"},
        {"Descrição": "Mercado", "Valor": 800.0, "Tipo": "fixa", "Categoria": "Alimentação"},
    ]
    tool.list_fixed_expenses.return_value = [
        {"Descrição": "Aluguel", "Valor": "1500.00", "Tipo": "fixa", "Categoria": "Moradia"},
        {"Descrição": "Internet", "Valor": "100.00", "Tipo": "fixa", "Categoria": "Moradia"}
    ]
    tool.add_expense.return_value = {
        "Descrição": "Farmácia", "Valor": "85.50", "Tipo": "fixa", "Categoria": "Saúde"
    }
    return tool

@pytest.fixture
def mock_income_tool():
    tool = MagicMock()
    tool.service.get_incomes.return_value = [
        {"Descrição": "Salário", "Valor": 5000.0}
    ]
    tool.get_balance.return_value = {
        "total_receitas": 5000.0,
        "total_despesas": 2300.0,
        "saldo_liquido": 2700.0
    }
    tool.add_income.return_value = {
        "Descrição": "Freela", "Valor": "1200.00"
    }
    return tool

# --- Testes do TransactionAgent ---

def test_transaction_agent_can_handle():
    agent = TransactionAgent()
    assert agent.can_handle(AgentContext(message="add despesa Mercado 150")) >= 0.90
    assert agent.can_handle(AgentContext(message="ganhei 500 reais de freela")) >= 0.85
    assert agent.can_handle(AgentContext(message="qual o meu saldo?")) <= 0.20

def test_transaction_agent_process_pending():
    agent = TransactionAgent()
    res = agent.process(AgentContext(message="add despesa Supermercado 250.00"))
    assert res.agent_name == "transaction_agent"
    assert res.pending_transaction is not None
    assert res.pending_transaction["valor"] == 250.00
    assert "Supermercado" in res.pending_transaction["descricao"]
    assert "Confirmar" in res.suggested_actions

def test_transaction_agent_execute(mock_expense_tool, mock_income_tool):
    agent = TransactionAgent(expense_tool=mock_expense_tool, income_tool=mock_income_tool)
    msg = agent.execute_transaction({
        "action": "add_expense",
        "descricao": "Farmácia",
        "valor": 85.50,
        "tipo": "fixa",
        "categoria": "Saúde"
    })
    assert "confirmada com sucesso" in msg
    assert "Farmácia" in msg

# --- Testes do ReportAgent ---

def test_report_agent_can_handle():
    agent = ReportAgent()
    assert agent.can_handle(AgentContext(message="gerar relatorio executivo")) >= 0.95
    assert agent.can_handle(AgentContext(message="qual o meu saldo?")) >= 0.85
    assert agent.can_handle(AgentContext(message="comprei um cafe 10")) <= 0.20

def test_report_agent_process(mock_expense_tool, mock_income_tool):
    agent = ReportAgent(expense_tool=mock_expense_tool, income_tool=mock_income_tool)
    res = agent.process(AgentContext(message="relatório completo"))
    assert res.agent_name == "report_agent"
    assert res.report_data is not None
    assert res.report_data["total_receitas"] == 5000.0
    assert res.report_data["total_despesas"] == 2300.0
    assert res.report_data["saldo_liquido"] == 2700.0
    assert "Relatório Financeiro Executivo" in res.reply
    assert "Moradia" in res.report_data["despesas_por_categoria"]

def test_report_agent_balance_only(mock_expense_tool, mock_income_tool):
    agent = ReportAgent(expense_tool=mock_expense_tool, income_tool=mock_income_tool)
    res = agent.process(AgentContext(message="Qual o meu saldo atual?"))
    assert "Resumo do Saldo Atual" in res.reply
    assert "2700.00" in res.reply

# --- Testes do AdvisoryAgent ---

def test_advisory_agent_can_handle():
    agent = AdvisoryAgent()
    assert agent.can_handle(AgentContext(message="como economizar dinheiro este mês?")) >= 0.90
    assert agent.can_handle(AgentContext(message="add despesa 50")) <= 0.20

def test_advisory_agent_process(mock_expense_tool, mock_income_tool):
    agent = AdvisoryAgent(expense_tool=mock_expense_tool, income_tool=mock_income_tool)
    res = agent.process(AgentContext(message="preciso de uma dica de economia"))
    assert res.agent_name == "advisory_agent"
    assert "Diagnóstico e Consultoria Financeira" in res.reply
    assert "50 / 30 / 20" in res.reply

# --- Testes do GeneralFinancialAgent ---

def test_general_agent_math(mock_expense_tool):
    agent = GeneralFinancialAgent(api_key="", expense_tool=mock_expense_tool)
    assert agent.can_handle(AgentContext(message="dividir por 2 minhas despesas")) >= 0.85

    res = agent.process(AgentContext(message="dividir por 2 minhas despesas"))
    assert "Despesas Fixas Divididas por 2" in res.reply
    assert "750.00" in res.reply  # 1500 / 2
    assert "50.00" in res.reply   # 100 / 2

def test_general_agent_fallback():
    agent = GeneralFinancialAgent(api_key="")
    res = agent.process(AgentContext(message="Olá, tudo bem?"))
    assert res.agent_name == "general_agent"
    assert "Recebi sua mensagem" in res.reply

# --- Testes do Agente de Extensão (BudgetGoalAgent) ---

def test_budget_goal_agent_extension(mock_income_tool, mock_expense_tool):
    from src.agent.specialists.budget_goal_agent import BudgetGoalAgent
    from src.agent.router import AgentRouter

    goal_agent = BudgetGoalAgent(income_tool=mock_income_tool, expense_tool=mock_expense_tool)
    assert goal_agent.can_handle(AgentContext(message="minha meta é poupar R$ 1000")) >= 0.90

    res = goal_agent.process(AgentContext(message="minha meta é poupar R$ 1000"))
    assert res.agent_name == "budget_goal_agent"
    assert "Acompanhamento de Metas Financeiras" in res.reply
    assert "1000.00" in res.reply

    # Teste de registro dinâmico no AgentRouter sem alteração da API
    router = AgentRouter(expense_tool=mock_expense_tool, income_tool=mock_income_tool)
    router.registry.register(goal_agent)

    routed_res = router.route(AgentContext(message="quero bater minha meta de R$ 5000 este mês"))
    assert routed_res.agent_name == "budget_goal_agent"
    assert "Acompanhamento de Metas Financeiras" in routed_res.reply
