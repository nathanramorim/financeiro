"use client";

import React from "react";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { useApiStatus } from "@/components/layout/ApiStatusProvider";

export default function AssistentePage() {
  const { refreshApiStatus } = useApiStatus();

  return (
    <main className="max-w-4xl w-full mx-auto p-4 sm:p-6">
      <ChatContainer onDataChanged={refreshApiStatus} />
    </main>
  );
}
