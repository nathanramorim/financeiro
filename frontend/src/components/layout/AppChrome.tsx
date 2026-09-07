"use client";

import React from "react";
import { Topbar } from "@/components/ui/Topbar";
import { BottomNav } from "@/components/ui/BottomNav";
import { ApiStatusProvider, useApiStatus } from "./ApiStatusProvider";

const Chrome: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { apiStatus } = useApiStatus();

  return (
    <div className="min-h-screen flex flex-col bg-panel">
      <Topbar apiStatus={apiStatus} />
      <div className="flex-1 pb-20">{children}</div>
      <BottomNav />
    </div>
  );
};

export const AppChrome: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ApiStatusProvider>
    <Chrome>{children}</Chrome>
  </ApiStatusProvider>
);
