import React from "react";
import { Message, ReportData } from "@/domain/types";
import { TransactionConfirmCard } from "@/components/transactions/TransactionConfirmCard";
import { FinancialCharts } from "@/components/reports/FinancialCharts";
import { MarkdownRenderer } from "./MarkdownRenderer";

interface MessageBubbleProps {
  message: Message;
  onConfirmedTransaction?: (msg: string, updatedReport?: ReportData | null) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  onConfirmedTransaction,
}) => {
  const isUser = message.sender === "user";

  return (
    <div
      className={`flex flex-col my-2 max-w-[92%] sm:max-w-[85%] ${
        isUser ? "self-end items-end" : "self-start items-start"
      }`}
    >
      <div className="flex items-end gap-2">
        {!isUser && (
          <div className="w-7 h-7 rounded-btn bg-blue-50 text-primary flex items-center justify-center text-xs shrink-0 mb-1 border border-panel-border">
            🤖
          </div>
        )}

        <div
          className={`p-3.5 rounded-card text-sm leading-relaxed shadow-sm ${
            isUser
              ? "bg-primary text-white rounded-br-none"
              : "bg-white text-text border border-panel-border rounded-bl-none"
          }`}
        >
          {isUser ? (
            <div className="whitespace-pre-wrap break-words">{message.text}</div>
          ) : (
            <MarkdownRenderer content={message.text} />
          )}

          {/* Se a mensagem incluir ação pendente de confirmação */}
          {!isUser && message.pendingAction && (
            <TransactionConfirmCard
              action={message.pendingAction}
              onConfirmed={(resultMsg, updatedReport) => {
                if (onConfirmedTransaction) {
                  onConfirmedTransaction(resultMsg, updatedReport);
                }
              }}
            />
          )}

          {/* Se a mensagem for um relatório com gráficos */}
          {!isUser && message.isReport && message.reportData && (
            <FinancialCharts data={message.reportData} />
          )}
        </div>
      </div>

      <span className="text-[10px] text-text-dim mt-1 px-1">
        {new Intl.DateTimeFormat("pt-BR", {
          hour: "2-digit",
          minute: "2-digit",
        }).format(message.timestamp)}
      </span>
    </div>
  );
};
