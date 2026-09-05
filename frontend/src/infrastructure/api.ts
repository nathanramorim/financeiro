import {
  ChatMessageResponse,
  ConfirmTransactionPayload,
  ConfirmTransactionResponse,
  FinancialSummary,
  ReportData,
} from "@/domain/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkApiHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });
    return res.ok;
  } catch {
    return false;
  }
}

export async function sendChatMessage(
  message: string,
  history: Array<{ role: string; content: string }> = []
): Promise<ChatMessageResponse> {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Erro na comunicação com o assistente (${res.status}): ${errText}`);
  }

  return res.json();
}

export async function fetchFinancialSummary(): Promise<FinancialSummary> {
  const res = await fetch(`${API_BASE_URL}/api/transactions`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Erro ao obter resumo financeiro: ${res.status}`);
  }

  return res.json();
}

export async function confirmTransaction(
  payload: ConfirmTransactionPayload
): Promise<ConfirmTransactionResponse> {
  const res = await fetch(`${API_BASE_URL}/api/transactions/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Erro ao confirmar transação (${res.status}): ${errText}`);
  }

  return res.json();
}

export async function fetchReports(): Promise<ReportData> {
  const res = await fetch(`${API_BASE_URL}/api/reports`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Erro ao buscar relatórios: ${res.status}`);
  }

  return res.json();
}
