from unittest.mock import MagicMock
import gspread
from src.services.sheets import SheetsService, EXPECTED_STRUCTURE
from src.tools.expenses import ExpenseTool
from src.tools.income import IncomeTool

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
    assert balance["total_receitas"] >= balance["total_despesas"]

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
