from unittest.mock import MagicMock
import gspread
from backend.services.sheets import SheetsService, EXPECTED_STRUCTURE
from backend.tools.expenses import ExpenseTool
from backend.tools.income import IncomeTool


def _reset_expenses_cache():
    SheetsService._cached_expenses = None
    SheetsService._cached_expenses_time = 0


def _mocked_service_with_worksheet(monkeypatch, tmp_path, get_all_records_return):
    """Cria um SheetsService com self.sheet mockado e CACHE_FILE isolado em tmp_path."""
    monkeypatch.setattr("backend.services.sheets.CACHE_FILE", tmp_path / "sheets_backup.json")
    service = SheetsService(credentials_path="non_existent.json")
    mock_worksheet = MagicMock()
    mock_worksheet.get_all_records.return_value = get_all_records_return
    mock_sheet = MagicMock()
    mock_sheet.worksheet.return_value = mock_worksheet
    service.sheet = mock_sheet
    return service, mock_worksheet

def test_sheets_service_initial_records():
    service = SheetsService(credentials_path="non_existent.json")
    expenses = service.get_expenses()
    assert len(expenses) >= 2

def test_expense_tool_list_fixed():
    tool = ExpenseTool(sheets_service=SheetsService(credentials_path="non_existent.json"))
    fixed = tool.list_fixed_expenses()
    assert all(e["Tipo"] == "fixa" for e in fixed)

def test_expense_tool_add():
    service = SheetsService(credentials_path="non_existent.json")
    tool = ExpenseTool(sheets_service=service)
    new_expense = tool.add_expense("Academia", 100.0, tipo="fixa")
    assert new_expense["Categoria"] == "Outros" or new_expense["Categoria"] == "Saúde"
    
    fixed = tool.list_fixed_expenses()
    assert any(e["Descrição"] == "Academia" for e in fixed)

def test_income_tool_balance():
    service = SheetsService(credentials_path="non_existent.json")
    income_tool = IncomeTool(sheets_service=service)
    balance = income_tool.get_balance()
    assert "saldo_liquido" in balance
    assert balance["saldo_liquido"] == round(balance["total_receitas"] - balance["total_despesas"], 2)

def test_ensure_structure_creates_missing_worksheets():
    service = SheetsService(credentials_path="non_existent.json")
    mock_sheet = MagicMock()
    mock_sheet.worksheet.side_effect = gspread.exceptions.WorksheetNotFound
    
    mock_worksheet = MagicMock()
    mock_sheet.add_worksheet.return_value = mock_worksheet

    service.sheet = mock_sheet
    service.ensure_structure()

    assert mock_sheet.add_worksheet.call_count == 2
    mock_worksheet.append_row.assert_any_call(EXPECTED_STRUCTURE["Despesas"])
    mock_worksheet.append_row.assert_any_call(EXPECTED_STRUCTURE["Receitas"])


def test_zeroed_sheet_propagates_empty_list_to_cache_and_backup(monkeypatch, tmp_path):
    _reset_expenses_cache()
    service, mock_worksheet = _mocked_service_with_worksheet(monkeypatch, tmp_path, [])

    result = service.get_expenses()

    assert result == []
    assert SheetsService._cached_expenses == []
    assert service._in_memory_db["Despesas"] == []


def test_cache_hit_reused_for_empty_list_within_ttl(monkeypatch, tmp_path):
    _reset_expenses_cache()
    service, mock_worksheet = _mocked_service_with_worksheet(monkeypatch, tmp_path, [])

    first = service.get_expenses()
    second = service.get_expenses()

    assert first == []
    assert second == []
    assert mock_worksheet.get_all_records.call_count == 1


def test_fallback_after_exception_does_not_resurrect_stale_data(monkeypatch, tmp_path):
    _reset_expenses_cache()
    service, mock_worksheet = _mocked_service_with_worksheet(monkeypatch, tmp_path, [])
    service._in_memory_db["Despesas"] = [
        {"Descrição": "Antiga", "Valor": 100.0, "Tipo": "fixa", "Categoria": "Outros", "Data": "2026-01-01"}
    ]

    zeroed = service.get_expenses()
    assert zeroed == []

    # Expira o cache e simula falha de conexão na próxima leitura
    SheetsService._cached_expenses_time = 0
    mock_worksheet.get_all_records.side_effect = Exception("API indisponível")

    result_after_failure = service.get_expenses()

    assert result_after_failure == []
