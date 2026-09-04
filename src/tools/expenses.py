from src.services.sheets import SheetsService
from src.tools.category import CategoryTool

class ExpenseTool:
    def __init__(self, sheets_service: SheetsService = None):
        self.service = sheets_service or SheetsService()

    def list_fixed_expenses(self) -> list[dict]:
        return self.service.get_expenses(tipo_filtro="fixa")

    def list_all_expenses(self) -> list[dict]:
        return self.service.get_expenses()

    def add_expense(self, descricao: str, valor: float, tipo: str = "fixa", categoria: str = None) -> dict:
        if not categoria:
            categoria = CategoryTool.categorize(descricao)
        return self.service.add_expense(descricao=descricao, valor=valor, tipo=tipo, categoria=categoria)
