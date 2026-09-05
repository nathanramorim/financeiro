"use client";

import React, { useState, useRef, useEffect } from "react";
import { Message, ReportData } from "@/domain/types";
import { MessageBubble } from "./MessageBubble";
import { LoadingIndicator } from "./LoadingIndicator";
import { Button } from "@/components/ui/Button";
import { sendChatMessage } from "@/infrastructure/api";

interface ChatContainerProps {
  onDataChanged?: () => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ onDataChanged }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      sender: "assistant",
      text: "Olá! 👋 Sou seu assistente financeiro pessoal.\nPosso consultar seu saldo, registrar despesas/receitas, categorizar gastos e gerar relatórios completos com gráficos.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend?: string) => {
    const messageText = (textToSend || input).trim();
    if (!messageText || loading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!textToSend) setInput("");
    setLoading(true);

    try {
      // Prepara histórico recente para contexto
      const historyPayload = messages.slice(-6).map((m) => ({
        role: m.sender === "user" ? "user" : "assistant",
        content: m.text,
      }));

      const res = await sendChatMessage(messageText, historyPayload);

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        sender: "assistant",
        text: res.response,
        pendingAction: res.pending_action,
        isReport: res.is_report,
        reportData: res.report_data,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : "Não foi possível processar.";
      const errorMessage: Message = {
        id: `err-${Date.now()}`,
        sender: "assistant",
        text: `⚠️ Erro de conexão com a API: ${errMsg}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmed = (resultMsg: string, updatedReport?: ReportData | null) => {
    const confirmFeedback: Message = {
      id: `feedback-${Date.now()}`,
      sender: "assistant",
      text: resultMsg,
      isReport: !!updatedReport,
      reportData: updatedReport,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, confirmFeedback]);
    if (onDataChanged) {
      onDataChanged();
    }
  };

  const quickActions = [
    { label: "📊 Relatório Geral", cmd: "relatorio" },
    { label: "💰 Consultar Saldo", cmd: "qual o meu saldo atual?" },
    { label: "📋 Despesas Fixas", cmd: "listar despesas fixas" },
    { label: "➕ Add Despesa", cmd: "Add despesa Mercado 150" },
  ];

  return (
    <div className="flex flex-col h-[75vh] sm:h-[680px] bg-white rounded-card border border-panel-border shadow-sm overflow-hidden">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 flex flex-col space-y-1">
        {messages.map((m) => (
          <MessageBubble
            key={m.id}
            message={m}
            onConfirmedTransaction={handleConfirmed}
          />
        ))}

        {loading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Action Chips (Mobile-friendly horizontal scroll) */}
      <div className="px-4 py-2 bg-panel border-t border-panel-border flex items-center gap-1.5 overflow-x-auto no-scrollbar text-xs">
        <span className="text-[11px] text-text-dim font-medium shrink-0">Sugestões:</span>
        {quickActions.map((action) => (
          <button
            key={action.cmd}
            onClick={() => handleSend(action.cmd)}
            disabled={loading}
            className="px-2.5 py-1 bg-white hover:bg-slate-50 border border-panel-border text-text rounded-pill whitespace-nowrap transition-colors shadow-2xs font-medium cursor-pointer"
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-3 sm:p-4 bg-white border-t border-panel-border flex items-center gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Digite sua mensagem (ex: relatorio, saldo, add despesa...)"
          disabled={loading}
          className="flex-1 px-4 py-2.5 text-sm bg-panel border border-panel-border rounded-btn text-text placeholder-text-dim focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
        />
        <Button
          type="submit"
          variant="primary"
          size="md"
          disabled={loading || !input.trim()}
          className="shrink-0 font-bold px-4 sm:px-6"
        >
          {loading ? "..." : "Enviar"}
        </Button>
      </form>
    </div>
  );
};
