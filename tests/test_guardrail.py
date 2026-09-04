import pytest
from src.guardrail.validator import GuardrailValidator, GuardrailResult

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
