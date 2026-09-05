import React from "react";
import { Card } from "./Card";

interface StatTileProps {
  title: string;
  value: number;
  type?: "balance" | "income" | "expense";
  subtitle?: string;
}

export const StatTile: React.FC<StatTileProps> = ({
  title,
  value,
  type = "balance",
  subtitle,
}) => {
  const formattedValue = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);

  const textColors = {
    balance: value >= 0 ? "text-primary" : "text-danger",
    income: "text-success",
    expense: "text-danger",
  };

  const bgColors = {
    balance: "bg-blue-50/70 border-blue-100",
    income: "bg-emerald-50/70 border-emerald-100",
    expense: "bg-rose-50/70 border-rose-100",
  };

  return (
    <Card className={`flex flex-col justify-between border ${bgColors[type]}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-text-dim uppercase tracking-wider">
          {title}
        </span>
      </div>
      <div className={`text-xl sm:text-2xl font-bold ${textColors[type]} tracking-tight`}>
        {formattedValue}
      </div>
      {subtitle && (
        <div className="mt-1 text-xs text-text-dim">
          {subtitle}
        </div>
      )}
    </Card>
  );
};
