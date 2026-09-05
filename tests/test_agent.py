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

def test_agent_fallback_add_despesa_short_command():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("add despesa Restaurante 85.50")
    assert "Despesa cadastrada com sucesso" in response
    assert "Restaurante" in response
    assert "85.50" in response

def test_agent_detect_mutation_intent():
    agent = FinancialAgent(api_key="")
    
    tx_exp = agent.detect_mutation_intent("add despesa Supermercado 250.00")
    assert tx_exp is not None
    assert tx_exp["action"] == "add_expense"
    assert tx_exp["descricao"] == "Supermercado"
    assert tx_exp["valor"] == 250.00

    tx_inc = agent.detect_mutation_intent("atualizar receita Salario 6000.00")
    assert tx_inc is not None
    assert tx_inc["action"] == "update_income"
    assert tx_inc["descricao"] == "Salario"
    assert tx_inc["valor"] == 6000.00

    tx_none = agent.detect_mutation_intent("Qual o meu saldo?")
    assert tx_none is None

def test_agent_execute_transaction():
    agent = FinancialAgent(api_key="")
    tx = {
        "action": "add_expense",
        "action_label": "Adicionar Despesa",
        "descricao": "Academia",
        "valor": 120.00,
        "categoria": "Saúde",
        "tipo": "fixa"
    }
    response = agent.execute_transaction(tx)
    assert "Despesa cadastrada e confirmada com sucesso" in response
    assert "Academia" in response
def test_agent_is_report_request():
    agent = FinancialAgent(api_key="")
    assert agent.is_report_request("gerar relatorio") is True
    assert agent.is_report_request("exibir gráficos") is True
    assert agent.is_report_request("Qual o meu saldo?") is False

def test_agent_generate_report_data():
    agent = FinancialAgent(api_key="")
    report = agent.generate_report_data()
    assert "total_receitas" in report
    assert "total_despesas" in report
    assert "saldo_liquido" in report
    assert "despesas_por_categoria" in report
    assert isinstance(report["despesas_por_categoria"], dict)

def test_agent_process_message_report():
    agent = FinancialAgent(api_key="")
    response = agent.process_message("relatorio")
    assert "Relatório Financeiro Executivo" in response
    assert "Total de Receitas" in response
    assert "Total de Despesas" in response




