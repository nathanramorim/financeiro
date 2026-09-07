"use client";

import React, { useState, useEffect, useCallback } from "react";
import { StatTile } from "@/components/ui/StatTile";
import { FinancialCharts } from "@/components/reports/FinancialCharts";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useApiStatus } from "@/components/layout/ApiStatusProvider";
import { fetchFinancialSummary, fetchReports } from "@/infrastructure/api";
import { FinancialSummary, ReportData } from "@/domain/types";

export default function HomePage() {
  const { apiStatus, refreshApiStatus } = useApiStatus();
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [reports, setReports] = useState<ReportData | null>(null);

  const loadData = useCallback(async () => {
    if (apiStatus !== "online") {
      return;
    }

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
  }, [apiStatus]);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, [loadData]);

  return (
    <main className="max-w-4xl w-full mx-auto p-4 sm:p-6 space-y-5">
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
            onClick={refreshApiStatus}
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

      {/* Painel Analítico & Gráficos */}
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
    </main>
  );
}
