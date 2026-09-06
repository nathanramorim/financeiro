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

    @staticmethod
    def parse_float(val) -> float:
        """
        Converte com segurança inteiros, floats e strings numéricas (formatos PT-BR e US) em float.
        Ex: '85,5' -> 85.5, '1.500,50' -> 1500.50, '1,500.50' -> 1500.50, 1500 -> 1500.0
        """
        if val is None:
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip()
        if not val_str:
            return 0.0
        
        # Se contém vírgula e ponto (ex: 1.500,50 ou 1,500.50)
        if ',' in val_str and '.' in val_str:
            if val_str.rfind(',') > val_str.rfind('.'):
                # Formato PT-BR: 1.500,50 -> 1500.50
                val_str = val_str.replace('.', '').replace(',', '.')
            else:
                # Formato US: 1,500.50 -> 1500.50
                val_str = val_str.replace(',', '')
        elif ',' in val_str:
            # Formato PT-BR decimal: 85,5 ou 85,50 -> 85.5
            val_str = val_str.replace(',', '.')
        
        try:
            return float(val_str)
        except ValueError:
            return 0.0

