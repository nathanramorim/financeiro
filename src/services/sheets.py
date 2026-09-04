import os
import gspread
from google.oauth2.service_account import Credentials
from src.config import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEET_NAME

EXPECTED_STRUCTURE = {
    "Despesas": ["Descrição", "Valor", "Tipo", "Categoria", "Data"],
    "Receitas": ["Descrição", "Valor", "Data"]
}

class SheetsService:
    """Serviço de persistência integrado ao Google Sheets com inicialização automática de estrutura e fallback."""

    def __init__(self, credentials_path: str = GOOGLE_SHEETS_CREDENTIALS_FILE, sheet_name: str = GOOGLE_SHEET_NAME):
        self.credentials_path = credentials_path
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self._in_memory_db = {
            "Despesas": [
                {"Descrição": "Aluguel", "Valor": 1500.0, "Tipo": "fixa", "Categoria": "Moradia", "Data": "2026-09-01"},
                {"Descrição": "Internet", "Valor": 120.0, "Tipo": "fixa", "Categoria": "Moradia", "Data": "2026-09-02"}
            ],
            "Receitas": [
                {"Descrição": "Salário", "Valor": 5000.0, "Data": "2026-09-01"}
            ]
        }
        self._connect()

    def _connect(self):
        if os.path.exists(self.credentials_path):
            try:
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
                self.client = gspread.authorize(creds)
                self.sheet = self.client.open(self.sheet_name)
                self.ensure_structure()
            except Exception as e:
                print(f"[SheetsService Warning] Falha ao conectar via gspread: {e}. Usando armazenamento em memória.")
                self.client = None
        else:
            print("[SheetsService Info] Arquivo de credenciais não encontrado. Usando repositório em memória para testes.")

    def ensure_structure(self):
        """Garante que as abas 'Despesas' e 'Receitas' existam com seus cabeçalhos corretos (idempotente)."""
        if not self.sheet:
            return

        for title, expected_headers in EXPECTED_STRUCTURE.items():
            try:
                worksheet = self.sheet.worksheet(title)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = self.sheet.add_worksheet(title=title, rows=100, cols=len(expected_headers))
                worksheet.append_row(expected_headers)
                print(f"[SheetsService Info] Aba '{title}' criada com cabeçalhos.")
                continue
            except Exception as e:
                print(f"[SheetsService Error] Erro ao acessar aba '{title}': {e}")
                continue

            try:
                first_row = worksheet.row_values(1)
                if first_row != expected_headers:
                    if not first_row:
                        worksheet.append_row(expected_headers)
                    else:
                        worksheet.update(range_name="A1", values=[expected_headers])
                    print(f"[SheetsService Info] Cabeçalhos da aba '{title}' inicializados/atualizados.")
            except Exception as e:
                print(f"[SheetsService Error] Erro ao verificar cabeçalhos da aba '{title}': {e}")

    def get_expenses(self, tipo_filtro: str = None) -> list[dict]:
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Despesas")
                records = worksheet.get_all_records()
                if tipo_filtro:
                    return [r for r in records if r.get("Tipo", "").lower() == tipo_filtro.lower()]
                return records
            except Exception as e:
                print(f"[SheetsService Error] Erro ao ler despesas: {e}")
        
        records = self._in_memory_db["Despesas"]
        if tipo_filtro:
            return [r for r in records if r.get("Tipo", "").lower() == tipo_filtro.lower()]
        return records

    def add_expense(self, descricao: str, valor: float, tipo: str = "fixa", categoria: str = "Outros", data: str = "2026-09-04") -> dict:
        item = {
            "Descrição": descricao,
            "Valor": float(valor),
            "Tipo": tipo,
            "Categoria": categoria,
            "Data": data
        }
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Despesas")
                worksheet.append_row([descricao, valor, tipo, categoria, data])
            except Exception as e:
                print(f"[SheetsService Error] Erro ao cadastrar despesa: {e}")

        self._in_memory_db["Despesas"].append(item)
        return item

    def get_incomes(self) -> list[dict]:
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Receitas")
                return worksheet.get_all_records()
            except Exception as e:
                print(f"[SheetsService Error] Erro ao ler receitas: {e}")

        return self._in_memory_db["Receitas"]

    def add_income(self, descricao: str, valor: float, data: str = "2026-09-04") -> dict:
        item = {
            "Descrição": descricao,
            "Valor": float(valor),
            "Data": data
        }
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Receitas")
                worksheet.append_row([descricao, valor, data])
            except Exception as e:
                print(f"[SheetsService Error] Erro ao cadastrar receita: {e}")

        self._in_memory_db["Receitas"].append(item)
        return item

    def get_balance(self) -> dict:
        expenses = self.get_expenses()
        incomes = self.get_incomes()

        total_expenses = sum(float(e.get("Valor", 0)) for e in expenses)
        total_incomes = sum(float(i.get("Valor", 0)) for i in incomes)
        balance = total_incomes - total_expenses

        return {
            "total_receitas": round(total_incomes, 2),
            "total_despesas": round(total_expenses, 2),
            "saldo_liquido": round(balance, 2)
        }
