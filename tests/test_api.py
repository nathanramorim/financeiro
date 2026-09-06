import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.api.main import app
from backend.api.routes import get_agent

@pytest.fixture
def mock_agent():
    agent = MagicMock()
    agent.process_message.return_value = "Mensagem processada pelo agente."
    agent.detect_mutation_intent.return_value = None
    agent.is_report_request.return_value = False
    agent.generate_report_data.return_value = {
        "total_receitas": 5000.0,
        "total_despesas": 2000.0,
        "saldo_liquido": 3000.0,
        "despesas_por_categoria": {"Alimentação": 500.0, "Moradia": 1500.0}
    }
    agent.expense_tool.list_all_expenses.return_value = [
        {"Descrição": "Aluguel", "Valor": 1500.0, "Tipo": "fixa", "Categoria": "Moradia"},
        {"Descrição": "Mercado", "Valor": 500.0, "Tipo": "fixa", "Categoria": "Alimentação"}
    ]
    agent.income_tool.service.get_incomes.return_value = [
        {"Descrição": "Salário", "Valor": 5000.0}
    ]
    agent.execute_transaction.return_value = "✅ Despesa cadastrada e confirmada com sucesso!"
    return agent

@pytest.fixture
def client(mock_agent):
    app.dependency_overrides[get_agent] = lambda: mock_agent
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "financeiro-api"}

def test_chat_out_of_scope_guardrail(client):
    response = client.post("/api/chat", json={"message": "Qual a previsão do tempo em Paris amanhã?"})
    assert response.status_code == 200
    data = response.json()
    assert "fora do escopo" in data["response"]
    assert data["pending_action"] is None
    assert data["is_report"] is False

def test_chat_mutation_intent_triggers_pending(mock_agent, client):
    mock_agent.detect_mutation_intent.return_value = {
        "action": "add_expense",
        "action_label": "Adicionar Despesa",
        "descricao": "Mercado",
        "valor": 150.0,
        "categoria": "Alimentação",
        "tipo": "fixa"
    }

    response = client.post("/api/chat", json={"message": "Add despesa Mercado 150"})
    assert response.status_code == 200
    data = response.json()
    assert data["pending_action"] is not None
    assert data["pending_action"]["valor"] == 150.0
    assert data["pending_action"]["descricao"] == "Mercado"
    assert "Deseja confirmar" in data["response"]

def test_chat_report_request(mock_agent, client):
    mock_agent.is_report_request.return_value = True
    response = client.post("/api/chat", json={"message": "relatorio"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_report"] is True
    assert data["report_data"] is not None
    assert data["report_data"]["total_receitas"] == 5000.0
    assert data["report_data"]["saldo_liquido"] == 3000.0

def test_get_transactions(client):
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.json()
    assert data["total_receitas"] == 5000.0
    assert data["total_despesas"] == 2000.0
    assert data["saldo_liquido"] == 3000.0
    assert len(data["fixed_expenses"]) == 2
    assert len(data["incomes"]) == 1
    assert data["despesas_por_categoria"]["Moradia"] == 1500.0

def test_confirm_transaction(client):
    payload = {
        "action": "add_expense",
        "descricao": "Farmácia",
        "valor": 85.5,
        "categoria": "Saúde",
        "tipo": "fixa"
    }
    response = client.post("/api/transactions/confirm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "confirmada com sucesso" in data["message"]
    assert data["report_data"] is not None

def test_get_reports(client):
    response = client.get("/api/reports")
    assert response.status_code == 200
    data = response.json()
    assert data["total_receitas"] == 5000.0
    assert data["total_despesas"] == 2000.0
    assert data["saldo_liquido"] == 3000.0
