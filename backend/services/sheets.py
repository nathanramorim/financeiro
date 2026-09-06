import os
import time
import json
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
from backend.config import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEET_NAME
from backend.tools.math_tool import MathTool

EXPECTED_STRUCTURE = {
    "Despesas": ["Descrição", "Valor", "Tipo", "Categoria", "Data"],
    "Receitas": ["Descrição", "Valor", "Data"]
}

CACHE_FILE = Path(".cache/sheets_backup.json")

class SheetsService:
    """Serviço de persistência integrado ao Google Sheets com cache TTL, backup local e fallback resiliente."""

    _cached_client = None
    _cached_sheet = None
    _cached_expenses = None
    _cached_expenses_time = 0
    _cached_incomes = None
    _cached_incomes_time = 0
    TTL_SECONDS = 30  # Reusa leitura por 30 segundos evitando estourar cota 429 do Google

    def __init__(self, credentials_path: str = GOOGLE_SHEETS_CREDENTIALS_FILE, sheet_name: str = GOOGLE_SHEET_NAME):
        self.credentials_path = credentials_path
        self.sheet_name = sheet_name
        self.client = SheetsService._cached_client
        self.sheet = SheetsService._cached_sheet
        self._in_memory_db = {
            "Despesas": [
                {"Descrição": "Aluguel", "Valor": 1500.0, "Tipo": "fixa", "Categoria": "Moradia", "Data": "2026-09-01"},
                {"Descrição": "Mercado", "Valor": 2455.0, "Tipo": "fixa", "Categoria": "Alimentação", "Data": "2026-09-02"},
                {"Descrição": "Academia", "Valor": 480.0, "Tipo": "fixa", "Categoria": "Saúde", "Data": "2026-09-03"},
                {"Descrição": "Uber", "Valor": 450.0, "Tipo": "fixa", "Categoria": "Transporte", "Data": "2026-09-03"}
            ],
            "Receitas": [
                {"Descrição": "Salário", "Valor": 10100.0, "Data": "2026-09-01"}
            ]
        }
        self._load_backup()
        if not self.sheet:
            self._connect()

    def _load_backup(self):
        try:
            if CACHE_FILE.exists():
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        if "Despesas" in data and data["Despesas"]:
                            self._in_memory_db["Despesas"] = data["Despesas"]
                        if "Receitas" in data and data["Receitas"]:
                            self._in_memory_db["Receitas"] = data["Receitas"]
        except Exception as e:
            print(f"[SheetsService Warning] Falha ao ler backup local: {e}")

    def _save_backup(self):
        try:
            CACHE_FILE.parent.mkdir(exist_ok=True, parents=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self._in_memory_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SheetsService Warning] Falha ao gravar backup local: {e}")

    def _connect(self):
        if os.path.exists(self.credentials_path):
            try:
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
                self.client = gspread.authorize(creds)
                SheetsService._cached_client = self.client
                try:
                    self.sheet = self.client.open(self.sheet_name)
                except Exception:
                    available = self.client.openall()
                    match = next((s for s in available if s.title in [self.sheet_name, "fin-agent", "FinancasPessoais"]), None)
                    if not match and available:
                        match = available[0]
                    if match:
                        print(f"[SheetsService Info] Conectado à planilha disponível '{match.title}'.")
                        self.sheet = match
                    else:
                        raise
                SheetsService._cached_sheet = self.sheet
                self.ensure_structure()
            except Exception as e:
                print(f"[SheetsService Warning] Falha ao conectar via gspread: {e}. Usando armazenamento em memória.")
                self.client = None
                self.sheet = None
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
                try:
                    worksheet = self.sheet.add_worksheet(title=title, rows=100, cols=len(expected_headers))
                    worksheet.append_row(expected_headers)
                    print(f"[SheetsService Info] Aba '{title}' criada com cabeçalhos.")
                except Exception as e:
                    print(f"[SheetsService Error] Erro ao criar aba '{title}': {e}")
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
        now = time.time()
        # Usa cache se válido dentro da janela de TTL
        if SheetsService._cached_expenses is not None and (now - SheetsService._cached_expenses_time < self.TTL_SECONDS):
            records = SheetsService._cached_expenses
        else:
            records = []
            if self.sheet:
                try:
                    worksheet = self.sheet.worksheet("Despesas")
                    records = worksheet.get_all_records(numericise_ignore=['all'])
                    if records:
                        self._in_memory_db["Despesas"] = records
                        SheetsService._cached_expenses = records
                        SheetsService._cached_expenses_time = now
                        self._save_backup()
                except Exception as e:
                    print(f"[SheetsService Error] Erro ao ler despesas: {e}")
                    records = self._in_memory_db["Despesas"]
            else:
                records = self._in_memory_db["Despesas"]

        sanitized = []
        for r in records:
            item = dict(r)
            item["Valor"] = MathTool.parse_float(item.get("Valor", 0))
            sanitized.append(item)

        if tipo_filtro:
            return [r for r in sanitized if str(r.get("Tipo", "")).lower() == tipo_filtro.lower()]
        return sanitized

    def add_expense(self, descricao: str, valor: float, tipo: str = "fixa", categoria: str = "Outros", data: str = "2026-09-04") -> dict:
        valor_parsed = MathTool.parse_float(valor)
        item = {
            "Descrição": descricao,
            "Valor": valor_parsed,
            "Tipo": tipo,
            "Categoria": categoria,
            "Data": data
        }
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Despesas")
                worksheet.append_row([descricao, valor_parsed, tipo, categoria, data])
            except Exception as e:
                print(f"[SheetsService Error] Erro ao cadastrar despesa: {e}")

        self._in_memory_db["Despesas"].append(item)
        self._save_backup()
        # Invalida cache de leitura para forçar atualização no próximo get
        SheetsService._cached_expenses_time = 0
        SheetsService._cached_expenses = None
        return item

    def get_incomes(self) -> list[dict]:
        now = time.time()
        if SheetsService._cached_incomes is not None and (now - SheetsService._cached_incomes_time < self.TTL_SECONDS):
            records = SheetsService._cached_incomes
        else:
            records = []
            if self.sheet:
                try:
                    worksheet = self.sheet.worksheet("Receitas")
                    records = worksheet.get_all_records(numericise_ignore=['all'])
                    if records:
                        self._in_memory_db["Receitas"] = records
                        SheetsService._cached_incomes = records
                        SheetsService._cached_incomes_time = now
                        self._save_backup()
                except Exception as e:
                    print(f"[SheetsService Error] Erro ao ler receitas: {e}")
                    records = self._in_memory_db["Receitas"]
            else:
                records = self._in_memory_db["Receitas"]

        sanitized = []
        for r in records:
            item = dict(r)
            item["Valor"] = MathTool.parse_float(item.get("Valor", 0))
            sanitized.append(item)

        return sanitized

    def add_income(self, descricao: str, valor: float, data: str = "2026-09-04") -> dict:
        valor_parsed = MathTool.parse_float(valor)
        item = {
            "Descrição": descricao,
            "Valor": valor_parsed,
            "Data": data
        }
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet("Receitas")
                worksheet.append_row([descricao, valor_parsed, data])
            except Exception as e:
                print(f"[SheetsService Error] Erro ao cadastrar receita: {e}")

        self._in_memory_db["Receitas"].append(item)
        self._save_backup()
        # Invalida cache de leitura para forçar atualização no próximo get
        SheetsService._cached_incomes_time = 0
        SheetsService._cached_incomes = None
        return item

    def get_balance(self) -> dict:
        incomes = self.get_incomes()
        expenses = self.get_expenses()
        total_rec = sum(MathTool.parse_float(i.get("Valor", 0)) for i in incomes)
        total_desp = sum(MathTool.parse_float(e.get("Valor", 0)) for e in expenses)
        return {
            "total_receitas": round(total_rec, 2),
            "total_despesas": round(total_desp, 2),
            "saldo_liquido": round(total_rec - total_desp, 2)
        }
