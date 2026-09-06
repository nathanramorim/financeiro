import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.api.main import app
from backend.api.routes import get_agent
from backend.agent.router import AgentRouter

@pytest.fixture
def mock_multiagent_router():
    expense_tool = MagicMock()
    expense_tool.list_all_expenses.return_value = [
        {"Descrição": "Aluguel", "Valor": 1500.0, "Tipo": "fixa", "Categoria": "Moradia"},
        {"Descrição": "Mercado", "Valor": 800.0, "Tipo": "fixa", "Categoria": "Alimentação"},
    ]
    expense_tool.list_fixed_expenses.return_value = [
        {"Descrição": "Aluguel", "Valor": "1500.00", "Tipo": "fixa", "Categoria": "Moradia"},
        {"Descrição": "Internet", "Valor": "100.00", "Tipo": "fixa", "Categoria": "Moradia"}
    ]
    expense_tool.add_expense.return_value = {
        "Descrição": "Farmácia", "Valor": "85.50", "Tipo": "fixa", "Categoria": "Saúde"
    }

    income_tool = MagicMock()
    income_tool.service.get_incomes.return_value = [
        {"Descrição": "Salário", "Valor": 5000.0}
    ]
    income_tool.get_balance.return_value = {
        "total_receitas": 5000.0,
        "total_despesas": 2300.0,
        "saldo_liquido": 2700.0
    }
    income_tool.add_income.return_value = {
        "Descrição": "Freela", "Valor": "1200.00"
    }

    router = AgentRouter(expense_tool=expense_tool, income_tool=income_tool)
    return router

@pytest.fixture
def client(mock_multiagent_router):
    app.dependency_overrides[get_agent] = lambda: mock_multiagent_router
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_api_chat_transaction_routing(client):
    response = client.post("/api/chat", json={"message": "add despesa Farmácia 85.50"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "transaction_agent"
    assert data["pending_action"] is not None
    assert data["pending_action"]["valor"] == 85.50
    assert "Deseja confirmar" in data["response"]
    assert "Confirmar" in (data["suggested_actions"] or [])

def test_api_chat_report_routing(client):
    response = client.post("/api/chat", json={"message": "gerar relatorio executivo"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "report_agent"
    assert data["is_report"] is True
    assert data["report_data"] is not None
    assert data["report_data"]["total_receitas"] == 5000.0
    assert data["report_data"]["saldo_liquido"] == 2700.0
    assert "Relatório Financeiro Executivo" in data["response"]

def test_api_chat_advisory_routing(client):
    response = client.post("/api/chat", json={"message": "como economizar dinheiro?"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "advisory_agent"
    assert "Diagnóstico e Consultoria Financeira" in data["response"]
    assert "50 / 30 / 20" in data["response"]

def test_api_chat_general_math_routing(client):
    response = client.post("/api/chat", json={"message": "dividir por 2 minhas despesas"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "general_agent"
    assert "Despesas Fixas Divididas por 2" in data["response"]
    assert "750.00" in data["response"]

def test_api_chat_guardrail_out_of_scope(client):
    response = client.post("/api/chat", json={"message": "Qual é a capital da França?"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "guardrail"
    assert "fora do escopo" in data["response"]
    assert data["pending_action"] is None

def test_api_chat_general_concept_routing(client):
    response = client.post("/api/chat", json={"message": "o que é taxa selic?"})
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "general_agent"
    assert "Selic" in data["response"] or "selic" in data["response"].lower()
    assert "juros" in data["response"].lower()
