"use client";

import React, { createContext, useCallback, useContext, useEffect, useState } from "react";
import { checkApiHealth } from "@/infrastructure/api";

type ApiStatus = "online" | "offline" | "checking";

interface ApiStatusContextValue {
  apiStatus: ApiStatus;
  refreshApiStatus: () => Promise<boolean>;
}

const ApiStatusContext = createContext<ApiStatusContextValue | undefined>(undefined);

export const ApiStatusProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("checking");

  const refreshApiStatus = useCallback(async () => {
    const isHealthy = await checkApiHealth();
    setApiStatus(isHealthy ? "online" : "offline");
    return isHealthy;
  }, []);

  useEffect(() => {
    refreshApiStatus();
    const interval = setInterval(refreshApiStatus, 15000);
    return () => clearInterval(interval);
  }, [refreshApiStatus]);

  return (
    <ApiStatusContext.Provider value={{ apiStatus, refreshApiStatus }}>
      {children}
    </ApiStatusContext.Provider>
  );
};

export function useApiStatus(): ApiStatusContextValue {
  const ctx = useContext(ApiStatusContext);
  if (!ctx) {
    throw new Error("useApiStatus deve ser usado dentro de ApiStatusProvider");
  }
  return ctx;
}
