from src.services.sheets import SheetsService

class IncomeTool:
    def __init__(self, sheets_service: SheetsService = None):
        self.service = sheets_service or SheetsService()

    def get_balance(self) -> dict:
        return self.service.get_balance()

    def add_income(self, descricao: str, valor: float) -> dict:
        return self.service.add_income(descricao=descricao, valor=valor)
