import React from "react";
import { Badge } from "./Badge";

interface TopbarProps {
  apiStatus?: "online" | "offline" | "checking";
}

export const Topbar: React.FC<TopbarProps> = ({ apiStatus = "online" }) => {
  return (
    <header className="w-full bg-white border-b border-panel-border sticky top-0 z-30 px-4 py-3 sm:px-6">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-card bg-primary text-white flex items-center justify-center font-bold text-lg shadow-sm">
            💰
          </div>
          <div>
            <h1 className="text-base sm:text-lg font-bold text-text leading-tight">
              Financeiro IA
            </h1>
            <p className="text-xs text-text-dim hidden sm:block">
              Assistente inteligente de finanças pessoais
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {apiStatus === "online" && (
            <Badge variant="success" className="gap-1.5">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse"></span>
              Online
            </Badge>
          )}
          {apiStatus === "offline" && (
            <Badge variant="danger" className="gap-1.5">
              <span className="w-2 h-2 rounded-full bg-danger"></span>
              Offline
            </Badge>
          )}
          {apiStatus === "checking" && (
            <Badge variant="neutral" className="gap-1.5">
              <span className="w-2 h-2 rounded-full bg-slate-400"></span>
              Conectando...
            </Badge>
          )}
        </div>
      </div>
    </header>
  );
};
