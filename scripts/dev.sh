#!/usr/bin/env bash
set -e

echo "🚀 Iniciando Assistente Financeiro (FastAPI + Next.js)..."

# Função para encerrar subprocessos ao sair
cleanup() {
  echo ""
  echo "🛑 Encerrando servidores..."
  kill $(jobs -p) 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Inicia o backend FastAPI
echo "📦 Iniciando Backend FastAPI na porta 8000..."
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Aguarda inicialização do backend
sleep 2

# 2. Inicia o frontend Next.js
echo "💻 Iniciando Frontend Next.js na porta 3020..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

# Aguarda os processos
wait $BACKEND_PID $FRONTEND_PID
