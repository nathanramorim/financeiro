export interface PendingAction {
  action: string;
  action_label: string;
  descricao: string;
  valor: number;
  categoria?: string | null;
  tipo?: string | null;
}

export interface ReportData {
  total_receitas: number;
  total_despesas: number;
  saldo_liquido: number;
  despesas_por_categoria: Record<string, number>;
}

export interface ChatMessageRequest {
  message: string;
  history?: Array<{ role: string; content: string }>;
}

export interface ChatMessageResponse {
  response: string;
  pending_action?: PendingAction | null;
  is_report?: boolean;
  report_data?: ReportData | null;
}

export interface TransactionItem {
  descricao: string;
  valor: number;
  tipo?: string | null;
  categoria?: string | null;
}

export interface FinancialSummary {
  total_receitas: number;
  total_despesas: number;
  saldo_liquido: number;
  fixed_expenses: TransactionItem[];
  incomes: TransactionItem[];
  despesas_por_categoria: Record<string, number>;
}

export interface ConfirmTransactionPayload {
  action: string;
  descricao: string;
  valor: number;
  categoria?: string | null;
  tipo?: string | null;
}

export interface ConfirmTransactionResponse {
  success: boolean;
  message: string;
  report_data?: ReportData | null;
}

export interface Message {
  id: string;
  sender: "user" | "assistant";
  text: string;
  pendingAction?: PendingAction | null;
  isReport?: boolean;
  reportData?: ReportData | null;
  timestamp: Date;
}
