import React from "react";
import { ReportData } from "@/domain/types";
import { Card } from "@/components/ui/Card";

interface FinancialChartsProps {
  data: ReportData;
}

export const FinancialCharts: React.FC<FinancialChartsProps> = ({ data }) => {
  const maxBarValue = Math.max(data.total_receitas, data.total_despesas, 1);
  const receitaPercent = Math.round((data.total_receitas / maxBarValue) * 100);
  const despesaPercent = Math.round((data.total_despesas / maxBarValue) * 100);

  const categories = Object.entries(data.despesas_por_categoria || {});
  const maxCatValue = Math.max(...categories.map(([, val]) => val), 1);

  const formatBRL = (val: number) =>
    new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(val);

  const categoryColors = [
    "bg-primary",
    "bg-accent-indigo",
    "bg-accent-violet",
    "bg-warning",
    "bg-accent-blue-soft",
  ];

  return (
    <div className="space-y-4 my-4 w-full">
      {/* Gráfico 1: Receita vs Despesa */}
      <Card className="w-full">
        <h4 className="text-sm font-bold text-text mb-1">
          📊 Balanço Geral: Receita vs Despesa
        </h4>
        <p className="text-xs text-text-dim mb-4">
          Comparativo direto de entradas e saídas cadastradas
        </p>

        <div className="space-y-3">
          {/* Receitas */}
          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span className="text-success flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-success"></span>
                Receitas
              </span>
              <span className="text-text font-bold">{formatBRL(data.total_receitas)}</span>
            </div>
            <div className="w-full h-4 bg-slate-100 rounded-pill overflow-hidden">
              <div
                className="h-full bg-success transition-all duration-500 rounded-pill"
                style={{ width: `${receitaPercent}%` }}
              />
            </div>
          </div>

          {/* Despesas */}
          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span className="text-danger flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-danger"></span>
                Despesas
              </span>
              <span className="text-text font-bold">{formatBRL(data.total_despesas)}</span>
            </div>
            <div className="w-full h-4 bg-slate-100 rounded-pill overflow-hidden">
              <div
                className="h-full bg-danger transition-all duration-500 rounded-pill"
                style={{ width: `${despesaPercent}%` }}
              />
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-panel-border flex justify-between items-center text-xs">
          <span className="text-text-dim">Saldo Líquido:</span>
          <span
            className={`font-bold text-sm ${
              data.saldo_liquido >= 0 ? "text-primary" : "text-danger"
            }`}
          >
            {formatBRL(data.saldo_liquido)}
          </span>
        </div>
      </Card>

      {/* Gráfico 2: Despesas por Categoria */}
      {categories.length > 0 && (
        <Card className="w-full">
          <h4 className="text-sm font-bold text-text mb-1">
            🏷️ Despesas Fixas por Categoria
          </h4>
          <p className="text-xs text-text-dim mb-4">
            Distribuição de custos nas categorias cadastradas
          </p>

          <div className="space-y-3">
            {categories.map(([categoria, valor], index) => {
              const catPercent = Math.round((valor / maxCatValue) * 100);
              const colorClass = categoryColors[index % categoryColors.length];

              return (
                <div key={categoria} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-text font-medium">{categoria}</span>
                    <span className="text-text-dim font-bold">{formatBRL(valor)}</span>
                  </div>
                  <div className="w-full h-3 bg-slate-100 rounded-pill overflow-hidden">
                    <div
                      className={`h-full ${colorClass} transition-all duration-500 rounded-pill`}
                      style={{ width: `${catPercent}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}
    </div>
  );
};
