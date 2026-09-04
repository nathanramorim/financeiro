from dataclasses import dataclass
from src.guardrail.rules import FINANCIAL_KEYWORDS, OUT_OF_SCOPE_MSG

EXCLUDED_PHRASES = [
    "receita de", "bolo", "cozinha", "culinária", "comida", "piada", "poema", "futebol"
]

@dataclass
class GuardrailResult:
    is_valid: bool
    message: str

class GuardrailValidator:
    def __init__(self, keywords: list[str] = None):
        self.keywords = keywords if keywords is not None else FINANCIAL_KEYWORDS

    def validate(self, prompt: str) -> GuardrailResult:
        if not prompt or not prompt.strip():
            return GuardrailResult(is_valid=False, message="Prompt vazio.")

        prompt_lower = prompt.lower()
        
        # Se contiver frases expressamente fora de escopo (ex: culinária)
        if any(excluded in prompt_lower for excluded in EXCLUDED_PHRASES):
            return GuardrailResult(is_valid=False, message=OUT_OF_SCOPE_MSG)

        # Verifica contexto financeiro
        contains_financial_context = any(kw in prompt_lower for kw in self.keywords if kw != "receita")
        if "receita" in prompt_lower and not any(excluded in prompt_lower for excluded in EXCLUDED_PHRASES):
            contains_financial_context = True

        if not contains_financial_context:
            if "$" in prompt_lower or any(char.isdigit() for char in prompt_lower):
                contains_financial_context = True

        if contains_financial_context:
            return GuardrailResult(is_valid=True, message="Prompt válido.")
        else:
            return GuardrailResult(is_valid=False, message=OUT_OF_SCOPE_MSG)
