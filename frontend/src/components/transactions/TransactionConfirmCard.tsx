import React, { useState } from "react";
import { PendingAction, ReportData } from "@/domain/types";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { confirmTransaction } from "@/infrastructure/api";

interface TransactionConfirmCardProps {
  action: PendingAction;
  onConfirmed?: (resultMessage: string, updatedReport?: ReportData | null) => void;
  onCancelled?: () => void;
}

export const TransactionConfirmCard: React.FC<TransactionConfirmCardProps> = ({
  action,
  onConfirmed,
  onCancelled,
}) => {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"pending" | "confirmed" | "cancelled">("pending");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const formattedValue = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(action.valor);

  const isExpense = action.action.includes("expense");

  const handleConfirm = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const res = await confirmTransaction({
        action: action.action,
        descricao: action.descricao,
        valor: action.valor,
        categoria: action.categoria,
        tipo: action.tipo || "fixa",
      });
      setStatus("confirmed");
      if (onConfirmed) {
        onConfirmed(res.message, res.report_data);
      }
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : "Falha ao registrar transação.";
      setErrorMessage(errMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setStatus("cancelled");
    if (onCancelled) {
      onCancelled();
    }
  };

  if (status === "confirmed") {
    return (
      <Card className="bg-emerald-50/60 border-emerald-200 p-4 mt-2">
        <div className="flex items-center gap-2 text-success font-semibold text-sm">
          <span>✅ Transação confirmada e salva na planilha com sucesso!</span>
        </div>
      </Card>
    );
  }

  if (status === "cancelled") {
    return (
      <Card className="bg-slate-50 border-slate-200 p-3 mt-2 text-text-dim text-xs">
        <span>❌ Operação cancelada pelo usuário.</span>
      </Card>
    );
  }

  return (
    <Card highlight className="mt-3 border-panel-border-strong bg-white p-4">
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-text-dim">
            Confirmação Pendente
          </span>
          <h4 className="text-base font-bold text-text mt-0.5">
            {action.action_label}
          </h4>
        </div>
        <Badge variant={isExpense ? "danger" : "success"}>
          {isExpense ? "Despesa" : "Receita"}
        </Badge>
      </div>

      <div className="bg-panel rounded-btn p-3 mb-4 space-y-1.5 text-sm border border-panel-border">
        <div className="flex justify-between items-center">
          <span className="text-text-dim">Descrição:</span>
          <span className="font-semibold text-text">{action.descricao}</span>
        </div>
        {action.categoria && (
          <div className="flex justify-between items-center">
            <span className="text-text-dim">Categoria:</span>
            <Badge variant="neutral">{action.categoria}</Badge>
          </div>
        )}
        <div className="flex justify-between items-center pt-1 border-t border-panel-border/60">
          <span className="text-text-dim">Valor:</span>
          <span className={`text-base font-bold ${isExpense ? "text-danger" : "text-success"}`}>
            {formattedValue}
          </span>
        </div>
      </div>

      {errorMessage && (
        <div className="mb-3 text-xs text-danger font-medium bg-danger-bg p-2.5 rounded-btn border border-danger/20">
          {errorMessage}
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-2">
        <Button
          variant="success"
          size="md"
          fullWidth
          onClick={handleConfirm}
          disabled={loading}
          className="flex-1"
        >
          {loading ? "Salvando..." : "✅ Confirmar Registro"}
        </Button>
        <Button
          variant="outline"
          size="md"
          fullWidth
          onClick={handleCancel}
          disabled={loading}
          className="sm:w-auto"
        >
          Cancelar
        </Button>
      </div>
    </Card>
  );
};
