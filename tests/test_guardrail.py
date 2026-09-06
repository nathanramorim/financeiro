import pytest
from backend.guardrail.validator import GuardrailValidator

def test_guardrail_valid_financial_prompt():
    validator = GuardrailValidator()
    result = validator.validate("Quais são minhas despesas fixas deste mês?")
    assert result.is_valid is True

def test_guardrail_valid_prompt_with_currency():
    validator = GuardrailValidator()
    result = validator.validate("Divida por 2 a conta de 150 reais")
    assert result.is_valid is True

def test_guardrail_out_of_scope_prompt():
    validator = GuardrailValidator()
    result = validator.validate("Me dê uma receita de bolo de fubá")
    assert result.is_valid is False
    assert "fora do escopo" in result.message

def test_guardrail_empty_prompt():
    validator = GuardrailValidator()
    result = validator.validate("")
    assert result.is_valid is False

def test_guardrail_valid_report_prompts():
    validator = GuardrailValidator()
    assert validator.validate("relatorio").is_valid is True
    assert validator.validate("relatório").is_valid is True
    assert validator.validate("gerar relatório com gráficos").is_valid is True
    assert validator.validate("exibir gráficos").is_valid is True

def test_guardrail_advisory_prompts():
    validator = GuardrailValidator()
    assert validator.validate("como economizar dinheiro este mês?").is_valid is True
    assert validator.validate("preciso de uma dica de planejamento").is_valid is True
    assert validator.validate("estou gastando muito ultimamente").is_valid is True
    assert validator.validate("como aplicar a regra 50/30/20?").is_valid is True
    assert validator.validate("como sair do déficit financeiro?").is_valid is True

def test_guardrail_budget_goal_prompts():
    validator = GuardrailValidator()
    assert validator.validate("quero criar uma meta de poupança").is_valid is True
    assert validator.validate("qual o meu teto orçamentário?").is_valid is True
    assert validator.validate("como montar uma reserva de emergência?").is_valid is True
    assert validator.validate("quero poupar mais todo mês").is_valid is True

def test_guardrail_market_concepts_prompts():
    validator = GuardrailValidator()
    assert validator.validate("o que é taxa selic?").is_valid is True
    assert validator.validate("como funciona o rendimento do cdi?").is_valid is True
    assert validator.validate("o que é inflação acumulada?").is_valid is True
    assert validator.validate("como começar a investir?").is_valid is True

def test_guardrail_strict_out_of_scope():
    validator = GuardrailValidator()
    assert validator.validate("qual a escalação do time de futebol?").is_valid is False
    assert validator.validate("me conte uma piada engraçada").is_valid is False
    assert validator.validate("escreva um poema sobre flores").is_valid is False
    assert validator.validate("qual a previsão do tempo para amanhã?").is_valid is False
