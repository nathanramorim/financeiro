from src.agent.engine import FinancialAgent

def test_agent_fallback_balance():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("Qual o meu saldo?")
    assert "Resumo do Saldo Atual" in response
    assert "Saldo Líquido" in response

def test_agent_fallback_divide():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("Divida por 2 minhas despesas")
    assert "Despesas Fixas Divididas por 2" in response
    assert "➔" in response

def test_agent_fallback_expenses():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("Listar despesas fixas")
    assert "Despesas Fixas Cadastradas" in response

def test_agent_fallback_add_expense():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("Adicionei despesa Mercado R$ 150.00")
    assert "Despesa cadastrada com sucesso" in response
    assert "Mercado" in response
    assert "150.00" in response

