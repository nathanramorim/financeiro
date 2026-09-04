import re

class MathTool:
    """Ferramenta para execução determinística e segura de cálculos numéricos."""

    @staticmethod
    def evaluate(expression: str) -> float:
        """
        Avalia expressões aritméticas simples contendo números e operadores +, -, *, /, ().
        Retorna o resultado como float.
        """
        if not expression or not expression.strip():
            raise ValueError("Expressão matemática vazia.")

        # Sanitiza expressão permitindo apenas caracteres aritméticos seguros
        clean_expr = re.sub(r"[^\d\.\+\-\*\/\(\)\s]", "", expression)

        if not clean_expr.strip():
            raise ValueError(f"Expressão inválida: '{expression}'")

        try:
            # Uso de eval restrito a escopo seguro sem globais/locais
            result = float(eval(clean_expr, {"__builtins__": None}, {}))
            return round(result, 2)
        except Exception as e:
            raise ValueError(f"Erro ao calcular expressão '{expression}': {str(e)}")

    @staticmethod
    def divide(amount: float, divisor: float) -> float:
        if divisor == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return round(amount / divisor, 2)

    @staticmethod
    def multiply(amount: float, factor: float) -> float:
        return round(amount * factor, 2)
