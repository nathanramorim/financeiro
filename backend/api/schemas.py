from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class PendingAction(BaseModel):
    action: str
    action_label: str
    descricao: str
    valor: float
    categoria: Optional[str] = None
    tipo: Optional[str] = "fixa"

class ReportData(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo_liquido: float
    despesas_por_categoria: Dict[str, float] = Field(default_factory=dict)

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: Optional[List[Dict[str, Any]]] = None

class ChatMessageResponse(BaseModel):
    response: str
    pending_action: Optional[PendingAction] = None
    is_report: bool = False
    report_data: Optional[ReportData] = None
    agent_name: Optional[str] = None
    suggested_actions: Optional[List[str]] = None

class TransactionItem(BaseModel):
    descricao: str
    valor: float
    tipo: Optional[str] = None
    categoria: Optional[str] = None

class ConfirmTransactionRequest(BaseModel):
    action: str
    descricao: str
    valor: float
    categoria: Optional[str] = None
    tipo: Optional[str] = "fixa"

class ConfirmTransactionResponse(BaseModel):
    success: bool
    message: str
    report_data: Optional[ReportData] = None

class FinancialSummaryResponse(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo_liquido: float
    fixed_expenses: List[TransactionItem]
    incomes: List[TransactionItem]
    despesas_por_categoria: Dict[str, float]
