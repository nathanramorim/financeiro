import React from "react";

export const LoadingIndicator: React.FC = () => {
  return (
    <div className="flex items-center gap-2 p-3 bg-white rounded-card border border-panel-border shadow-sm max-w-xs self-start my-2">
      <div className="w-6 h-6 rounded-btn bg-blue-50 text-primary flex items-center justify-center text-xs animate-bounce">
        🤖
      </div>
      <div className="flex items-center gap-1">
        <span className="text-xs text-text-dim font-medium">Processando</span>
        <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse"></span>
        <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse [animation-delay:200ms]"></span>
        <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse [animation-delay:400ms]"></span>
      </div>
    </div>
  );
};
