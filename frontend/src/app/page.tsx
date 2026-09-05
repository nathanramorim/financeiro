"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Topbar } from "@/components/ui/Topbar";
import { StatTile } from "@/components/ui/StatTile";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { FinancialCharts } from "@/components/reports/FinancialCharts";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import {
  checkApiHealth,
  fetchFinancialSummary,
  fetchReports,
} from "@/infrastructure/api";
import { FinancialSummary, ReportData } from "@/domain/types";

export default function HomePage() {
  const [apiStatus, setApiStatus] = useState<"online" | "offline" | "checking">("checking");
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [reports, setReports] = useState<ReportData | null>(null);
  const [activeTab, setActiveTab] = useState<"chat" | "dashboard">("chat");

  const loadData = useCallback(async () => {
    const isHealthy = await checkApiHealth();
    setApiStatus(isHealthy ? "online" : "offline");

    if (isHealthy) {
      try {
        const [sumData, repData] = await Promise.all([
          fetchFinancialSummary(),
          fetchReports(),
        ]);
        setSummary(sumData);
        setReports(repData);
      } catch (e) {
        console.error("Erro ao sincronizar dados com o backend:", e);
      }
    }
  }, []);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, [loadData]);

  return (
    <div className="min-h-screen flex flex-col bg-panel">
      {/* Topbar Fixa com status de conexão */}
      <Topbar apiStatus={apiStatus} />

      <main className="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-6 space-y-5">
        {/* Banner de aviso se o backend não estiver rodando */}
        {apiStatus === "offline" && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-xs text-danger">
            <div className="flex items-center gap-2">
              <span className="text-base">⚠️</span>
              <span>
                Backend FastAPI offline. Certifique-se de executar{" "}
                <code className="bg-white px-1 py-0.5 rounded font-mono">
                  uv run uvicorn src.api.main:app --reload
                </code>.
              </span>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={loadData}
              className="text-xs shrink-0 self-end sm:self-auto"
            >
              Tentar reconectar
            </Button>
          </div>
        )}

        {/* Métricas Financeiras Principais (Stat Tiles) */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <StatTile
            title="Saldo Líquido"
            value={summary?.saldo_liquido ?? 0}
            type="balance"
            subtitle="Receitas - Despesas"
          />
          <StatTile
            title="Total Receitas"
            value={summary?.total_receitas ?? 0}
            type="income"
            subtitle={`${summary?.incomes?.length ?? 0} proventos cadastrados`}
          />
          <StatTile
            title="Total Despesas"
            value={summary?.total_despesas ?? 0}
            type="expense"
            subtitle={`${summary?.fixed_expenses?.length ?? 0} despesas ativas`}
          />
        </section>

        {/* Navegação entre Chat e Painel (Mobile-friendly tabs) */}
        <div className="flex border-b border-panel-border pb-1 gap-2">
          <button
            onClick={() => setActiveTab("chat")}
            className={`px-4 py-2 text-sm font-semibold rounded-btn transition-colors cursor-pointer ${
              activeTab === "chat"
                ? "bg-white text-primary shadow-xs border border-panel-border"
                : "text-text-dim hover:text-text"
            }`}
          >
            💬 Chat com Assistente
          </button>
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-4 py-2 text-sm font-semibold rounded-btn transition-colors cursor-pointer ${
              activeTab === "dashboard"
                ? "bg-white text-primary shadow-xs border border-panel-border"
                : "text-text-dim hover:text-text"
            }`}
          >
            📊 Painel & Gráficos
          </button>
        </div>

        {/* Aba 1: Chat Inteligente com Assistente */}
        {activeTab === "chat" && (
          <section className="w-full">
            <ChatContainer onDataChanged={loadData} />
          </section>
        )}

        {/* Aba 2: Painel Analítico & Gráficos */}
        {activeTab === "dashboard" && (
          <section className="space-y-4">
            {reports ? (
              <FinancialCharts data={reports} />
            ) : (
              <Card className="p-6 text-center text-text-dim text-sm">
                Nenhum dado financeiro disponível no momento.
              </Card>
            )}

            {/* Listagem Resumida de Despesas Fixas */}
            {summary && summary.fixed_expenses.length > 0 && (
              <Card>
                <div className="flex justify-between items-center mb-3">
                  <h4 className="text-sm font-bold text-text">
                    📋 Despesas Fixas Cadastradas
                  </h4>
                  <Badge variant="neutral">
                    {summary.fixed_expenses.length} itens
                  </Badge>
                </div>
                <div className="divide-y divide-panel-border text-sm">
                  {summary.fixed_expenses.map((exp, idx) => (
                    <div
                      key={idx}
                      className="py-2.5 flex justify-between items-center"
                    >
                      <div>
                        <span className="font-medium text-text">
                          {exp.descricao}
                        </span>
                        {exp.categoria && (
                          <span className="ml-2 text-xs text-text-dim bg-panel px-1.5 py-0.5 rounded">
                            {exp.categoria}
                          </span>
                        )}
                      </div>
                      <span className="font-semibold text-danger">
                        {new Intl.NumberFormat("pt-BR", {
                          style: "currency",
                          currency: "BRL",
                        }).format(exp.valor)}
                      </span>
                    </div>
                  ))}
                </div>
              </Card>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
