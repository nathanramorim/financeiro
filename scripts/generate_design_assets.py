import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML_BANNER = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #ffffff;
      --panel: #f6f8fb;
      --panel-border: #e4e9f0;
      --panel-border-strong: #bfd3f5;
      --text: #0f172a;
      --text-dim: #5b6675;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --success: #16a34a;
      --success-bg: #dcfce7;
      --warning: #d97706;
      --warning-bg: #fef3c7;
      --danger: #dc2626;
      --danger-bg: #fee2e2;
      --accent-indigo: #4f46e5;
      --accent-violet: #7c3aed;
      --accent-blue-soft: #60a5fa;
      --radius: 14px;
      --radius-sm: 8px;
      --radius-pill: 999px;
      --font: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font);
      background: #f1f5f9;
      color: var(--text);
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 32px;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .banner-container {
      width: 1200px;
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: 20px;
      box-shadow: 0 12px 36px rgba(15, 23, 42, 0.06);
      overflow: hidden;
    }

    /* Top Header */
    .banner-header {
      background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
      padding: 36px 44px 28px 44px;
      border-bottom: 1px solid var(--panel-border);
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      color: var(--primary);
      background: #eff4ff;
      border: 1px solid var(--panel-border-strong);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      margin-bottom: 14px;
    }

    .header-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }

    .header-title h1 {
      font-size: 34px;
      font-weight: 900;
      color: var(--text);
      letter-spacing: -0.8px;
      margin-bottom: 8px;
    }

    .header-title p {
      font-size: 16px;
      color: var(--text-dim);
      font-weight: 500;
    }

    .header-badges {
      display: flex;
      gap: 10px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      font-weight: 700;
    }
    .badge-success { background: var(--success-bg); color: var(--success); }
    .badge-primary { background: #eff4ff; color: var(--primary); border: 1px solid var(--panel-border-strong); }

    /* Product Preview Body */
    .banner-body {
      padding: 36px 44px 40px 44px;
      background: var(--panel);
    }

    /* Stat Tiles */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-bottom: 26px;
    }

    .stat-card {
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius);
      padding: 18px 22px;
      transition: all 0.2s ease;
    }
    .stat-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-dim);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .stat-value {
      font-size: 28px;
      font-weight: 900;
      letter-spacing: -0.5px;
      line-height: 1.1;
      margin-bottom: 6px;
    }
    .stat-value.primary { color: var(--primary); }
    .stat-value.success { color: var(--success); }
    .stat-value.danger { color: var(--danger); }
    .stat-sub {
      font-size: 12px;
      font-weight: 500;
      color: var(--text-dim);
    }

    /* Main Content Layout */
    .preview-grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 22px;
    }

    .panel-card {
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius);
      padding: 24px;
    }

    .panel-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-subtitle {
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 20px;
    }

    /* Progress Bar Charts */
    .chart-group {
      margin-bottom: 16px;
    }
    .chart-header {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 6px;
    }
    .chart-bar-bg {
      width: 100%;
      height: 12px;
      background: #f1f5f9;
      border-radius: var(--radius-pill);
      overflow: hidden;
    }
    .chart-bar-fill {
      height: 100%;
      border-radius: var(--radius-pill);
    }
    .bar-success { background: var(--success); }
    .bar-danger { background: var(--danger); }
    .bar-primary { background: var(--primary); }
    .bar-indigo { background: var(--accent-indigo); }
    .bar-warning { background: var(--warning); }

    /* Chat Conversation */
    .chat-bubble {
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
    }
    .chat-bubble.user {
      align-items: flex-end;
    }
    .chat-bubble.bot {
      align-items: flex-start;
    }

    .bubble-content {
      padding: 12px 16px;
      border-radius: 12px;
      font-size: 13px;
      max-width: 90%;
      line-height: 1.5;
    }
    .bubble-user {
      background: var(--primary);
      color: #ffffff;
      border-bottom-right-radius: 4px;
      font-weight: 500;
    }
    .bubble-bot {
      background: #f8fafc;
      border: 1px solid var(--panel-border);
      color: var(--text);
      border-bottom-left-radius: 4px;
    }
    .agent-tag {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--accent-indigo);
      background: #eef2ff;
      border: 1px solid #e0e7ff;
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }

    /* Quick Suggestion Chips */
    .chips-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 14px;
    }
    .chip {
      font-size: 11px;
      font-weight: 600;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-pill);
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .chip.active {
      border-color: var(--panel-border-strong);
      color: var(--primary);
      background: #eff4ff;
    }
  </style>
</head>
<body>
  <div class="banner-container">
    <!-- Header -->
    <div class="banner-header">
      <div class="eyebrow">⚡ Arquitetura Multiagente Inteligente</div>
      <div class="header-row">
        <div class="header-title">
          <h1>Financeiro</h1>
          <p>Seu assistente financeiro pessoal com Next.js 15, FastAPI e Google Sheets</p>
        </div>
        <div class="header-badges">
          <span class="badge badge-success">● FastAPI Online :8000</span>
          <span class="badge badge-primary">Next.js 15 :3020</span>
        </div>
      </div>
    </div>

    <!-- Body -->
    <div class="banner-body">
      <!-- 3 Stat Tiles -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Saldo Líquido <span>💰</span></div>
          <div class="stat-value success">R$ 1.850,00</div>
          <div class="stat-sub">+12% em relação ao mês anterior</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total de Receitas <span>📈</span></div>
          <div class="stat-value primary">R$ 5.000,00</div>
          <div class="stat-sub">3 proventos cadastrados</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total de Despesas <span>📉</span></div>
          <div class="stat-value danger">R$ 3.150,00</div>
          <div class="stat-sub">63% do limite orçamentário</div>
        </div>
      </div>

      <!-- Preview Split: Gráficos vs Chat -->
      <div class="preview-grid">
        <!-- Gráficos Reais -->
        <div class="panel-card">
          <div class="panel-title">📊 Balanço Geral & Categorias</div>
          <div class="panel-subtitle">Visualização determinística sincronizada com a planilha</div>

          <div class="chart-group">
            <div class="chart-header">
              <span style="color: var(--success)">Receitas Totais</span>
              <span>R$ 5.000,00 (100%)</span>
            </div>
            <div class="chart-bar-bg">
              <div class="chart-bar-fill bar-success" style="width: 100%;"></div>
            </div>
          </div>

          <div class="chart-group">
            <div class="chart-header">
              <span style="color: var(--danger)">Despesas Totais</span>
              <span>R$ 3.150,00 (63%)</span>
            </div>
            <div class="chart-bar-bg">
              <div class="chart-bar-fill bar-danger" style="width: 63%;"></div>
            </div>
          </div>

          <div style="border-top: 1px solid var(--panel-border); margin: 18px 0 14px 0;"></div>

          <div class="chart-group">
            <div class="chart-header">
              <span style="color: var(--text)">Moradia & Aluguel</span>
              <span style="color: var(--text-dim)">R$ 1.800,00</span>
            </div>
            <div class="chart-bar-bg">
              <div class="chart-bar-fill bar-primary" style="width: 75%;"></div>
            </div>
          </div>

          <div class="chart-group">
            <div class="chart-header">
              <span style="color: var(--text)">Alimentação & Mercado</span>
              <span style="color: var(--text-dim)">R$ 950,00</span>
            </div>
            <div class="chart-bar-bg">
              <div class="chart-bar-fill bar-indigo" style="width: 40%;"></div>
            </div>
          </div>

          <div class="chart-group" style="margin-bottom: 0;">
            <div class="chart-header">
              <span style="color: var(--text)">Transporte & Combustível</span>
              <span style="color: var(--text-dim)">R$ 400,00</span>
            </div>
            <div class="chart-bar-bg">
              <div class="chart-bar-fill bar-warning" style="width: 20%;"></div>
            </div>
          </div>
        </div>

        <!-- Conversa Real com Agentes -->
        <div class="panel-card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="panel-title">💬 Interação com Agentes Especialistas</div>
            <div class="panel-subtitle">Roteamento automático pelo AgentRouter com Guardrails</div>

            <div class="chat-bubble user">
              <div class="bubble-content bubble-user">
                Qual é a minha meta de poupança atual?
              </div>
            </div>

            <div class="chat-bubble bot">
              <span class="agent-tag">🎯 BudgetGoalAgent</span>
              <div class="bubble-content bubble-bot">
                Sua meta é acumular <strong>R$ 10.000,00</strong> para Reserva de Emergência. Poupando seu saldo atual de <strong>R$ 1.850,00/mês</strong>, você atingirá seu objetivo em <strong>6 meses</strong>!
              </div>
            </div>
          </div>

          <!-- Sugestões Rápidas -->
          <div>
            <div style="font-size: 11px; font-weight: 700; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.8px;">Sugestões Rápidas</div>
            <div class="chips-row">
              <div class="chip active">📊 Relatório Geral</div>
              <div class="chip">📈 Taxa Selic</div>
              <div class="chip">💡 Dicas de Economia</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

HTML_ARQUITETURA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0d1117;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 24px;
      font-family: 'JetBrains Mono', -apple-system, BlinkMacSystemFont, monospace;
      -webkit-font-smoothing: antialiased;
    }

    /* Janela macOS */
    .terminal-window {
      width: 1040px;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.05);
      overflow: hidden;
    }

    /* Barra Superior macOS */
    .terminal-header {
      background: #21262d;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      border-bottom: 1px solid #30363d;
      position: relative;
    }

    .traffic-lights {
      display: flex;
      gap: 8px;
      z-index: 2;
    }

    .light {
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }
    .light-close { background: #ff5f56; border: 1px solid #e0443e; }
    .light-min { background: #ffbd2e; border: 1px solid #dea123; }
    .light-max { background: #27c93f; border: 1px solid #1aab29; }

    .window-title {
      position: absolute;
      left: 0;
      right: 0;
      text-align: center;
      font-size: 12px;
      color: #8b949e;
      font-weight: 600;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    /* Conteúdo do Terminal */
    .terminal-content {
      padding: 20px 24px;
      color: #c9d1d9;
      font-size: 13px;
      line-height: 1.35;
    }

    .prompt-line {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
      font-size: 13px;
    }
    .prompt-user { color: #58a6ff; font-weight: 700; }
    .prompt-dir { color: #7ee787; font-weight: 600; }
    .prompt-branch { color: #d2a8ff; font-weight: 600; }
    .prompt-cmd { color: #f0f6fc; font-weight: 700; }

    /* Caixa do Claude Code */
    .claude-box {
      color: #8b949e;
      margin-bottom: 14px;
    }
    .claude-tag {
      color: #58a6ff;
      font-weight: 700;
    }

    /* Diagrama ASCII */
    pre {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12.5px;
      line-height: 1.35;
      color: #8b949e;
    }

    .c-frame { color: #484f58; }
    .c-user { color: #58a6ff; font-weight: 700; }
    .c-front { color: #79c0ff; font-weight: 700; }
    .c-back { color: #f0883e; font-weight: 700; }
    .c-guard { color: #ffa657; font-weight: 700; }
    .c-router { color: #d2a8ff; font-weight: 700; }
    .c-agent { color: #58a6ff; font-weight: 700; }
    .c-data { color: #7ee787; font-weight: 700; }
    .c-llm { color: #ff7b72; font-weight: 700; }
    .c-sub { color: #8b949e; }
    .c-arrow { color: #58a6ff; font-weight: 700; }
    .c-ok { color: #7ee787; font-weight: 700; }

    /* Rodapé do Terminal */
    .terminal-footer {
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid #21262d;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: #8b949e;
    }

    .cursor {
      display: inline-block;
      width: 8px;
      height: 15px;
      background: #58a6ff;
      vertical-align: middle;
      animation: blink 1s infinite;
      margin-left: 6px;
    }
    @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
  </style>
</head>
<body>
  <div class="terminal-window">
    <div class="terminal-header">
      <div class="traffic-lights">
        <div class="light light-close"></div>
        <div class="light light-min"></div>
        <div class="light light-max"></div>
      </div>
      <div class="window-title">
        <span>nathan@macbook</span>
        <span style="color: #484f58">•</span>
        <span>~/git/financeiro (main)</span>
        <span style="color: #484f58">•</span>
        <span style="color: #58a6ff">claude code</span>
      </div>
    </div>

    <div class="terminal-content">
      <div class="prompt-line">
        <span class="prompt-user">nathan@mac</span>
        <span class="prompt-dir">~/financeiro</span>
        <span class="prompt-branch">(main)</span>
        <span style="color: #8b949e">❯</span>
        <span class="prompt-cmd">claude "desenhe a arquitetura do projeto"</span>
      </div>

      <pre class="claude-box">
<span class="c-frame">╭─</span> <span class="claude-tag">Claude Code</span> <span class="c-frame">──────────────────────────────────────────────────────────────────────────╮</span>
<span class="c-frame">│</span> Multi-Agent System Architecture • financeiro (FastAPI + Next.js 15)                    <span class="c-frame">│</span>
<span class="c-frame">╰────────────────────────────────────────────────────────────────────────────────────────╯</span></pre>

      <pre>
<span class="c-frame">┌────────────────────────────────────────────────────────────────────────────────────────┐</span>
<span class="c-frame">│</span>                                  <span class="c-user">USUÁRIO / BROWSER</span>                                     <span class="c-frame">│</span>
<span class="c-frame">└───────────────────────────────────────────┬────────────────────────────────────────────┘</span>
                                            <span class="c-arrow">│ HTTP / JSON (:3020)</span>
                                            <span class="c-arrow">▼</span>
<span class="c-frame">┌────────────────────────────────────────────────────────────────────────────────────────┐</span>
<span class="c-frame">│</span>                              <span class="c-front">FRONTEND (Next.js 15 — :3020)</span>                             <span class="c-frame">│</span>
<span class="c-frame">│</span>   • <span class="c-sub">ChatContainer com sugestões rápidas</span>      • <span class="c-sub">Renderização rica Markdown & Badges</span>     <span class="c-frame">│</span>
<span class="c-frame">│</span>   • <span class="c-sub">Painel Mobile-First & StatTiles</span>          • <span class="c-sub">Gráficos Determinísticos SVG</span>           <span class="c-frame">│</span>
<span class="c-frame">└───────────────────────────────────────────┬────────────────────────────────────────────┘</span>
                                            <span class="c-arrow">│ REST POST /api/chat (:8000)</span>
                                            <span class="c-arrow">▼</span>
<span class="c-frame">┌────────────────────────────────────────────────────────────────────────────────────────┐</span>
<span class="c-frame">│</span>                               <span class="c-back">BACKEND (FastAPI — :8000)</span>                                <span class="c-frame">│</span>
<span class="c-frame">│</span>                                                                                        <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">┌────────────────────────────────────────────────────────────────────────────────┐</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>                            <span class="c-guard">GUARDRAIL VALIDATOR</span>                                 <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>   • <span class="c-sub">Validação de escopo financeiro estrito</span>                                     <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>   • <span class="c-sub">Bloqueio de prompt injection e assuntos fora de contexto</span>                   <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">└───────────────────────────────────────┬────────────────────────────────────────┘</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>                                           <span class="c-ok">│ Mensagem Aprovada</span>                          <span class="c-frame">│</span>
<span class="c-frame">│</span>                                           <span class="c-ok">▼</span>                                            <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">┌────────────────────────────────────────────────────────────────────────────────┐</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>                               <span class="c-router">AGENT ROUTER</span>                                     <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>   • <span class="c-sub">Analisa a intenção e calcula afinidade de cada especialista</span>                <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">│</span>   • <span class="c-sub">Despacha para o especialista com maior score (BaseAgent)</span>                   <span class="c-frame">│</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>   <span class="c-frame">└───────────────────────────────────────┬────────────────────────────────────────┘</span>   <span class="c-frame">│</span>
<span class="c-frame">│</span>                                           <span class="c-frame">│</span>                                            <span class="c-frame">│</span>
<span class="c-frame">│</span>                 <span class="c-frame">┌─────────────────────────┼─────────────────────────┐</span>                  <span class="c-frame">│</span>
<span class="c-frame">│</span>                 <span class="c-arrow">▼</span>                         <span class="c-arrow">▼</span>                         <span class="c-arrow">▼</span>                  <span class="c-frame">│</span>
<span class="c-frame">│</span>        <span class="c-frame">┌──────────────────┐</span>      <span class="c-frame">┌──────────────────┐</span>      <span class="c-frame">┌──────────────────┐</span>        <span class="c-frame">│</span>
<span class="c-frame">│</span>        <span class="c-frame">│</span> <span class="c-agent">TransactionAgent</span> <span class="c-frame">│</span>      <span class="c-frame">│</span>   <span class="c-agent">ReportAgent</span>    <span class="c-frame">│</span>      <span class="c-frame">│</span>  <span class="c-agent">AdvisoryAgent</span>   <span class="c-frame">│</span>        <span class="c-frame">│</span>
<span class="c-frame">│</span>        <span class="c-frame">│</span> • <span class="c-sub">Entradas/Saídas</span><span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">Balanço geral</span>  <span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">Regra 50/30/20</span> <span class="c-frame">│</span>        <span class="c-frame">│</span>
<span class="c-frame">│</span>        <span class="c-frame">│</span> • <span class="c-sub">Categorização</span>  <span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">Gráficos SVG</span>   <span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">Consultoria</span>    <span class="c-frame">│</span>        <span class="c-frame">│</span>
<span class="c-frame">│</span>        <span class="c-frame">└────────┬─────────┘</span>      <span class="c-frame">└────────┬─────────┘</span>      <span class="c-frame">└────────┬─────────┘</span>        <span class="c-frame">│</span>
<span class="c-frame">│</span>                 <span class="c-frame">│</span>                         <span class="c-frame">│</span>                         <span class="c-frame">│</span>                  <span class="c-frame">│</span>
<span class="c-frame">│</span>                 <span class="c-frame">└────────────┬────────────┴────────────┬────────────┘</span>                  <span class="c-frame">│</span>
<span class="c-frame">│</span>                              <span class="c-arrow">▼</span>                         <span class="c-arrow">▼</span>                               <span class="c-frame">│</span>
<span class="c-frame">│</span>                     <span class="c-frame">┌──────────────────┐</span>      <span class="c-frame">┌──────────────────┐</span>                     <span class="c-frame">│</span>
<span class="c-frame">│</span>                     <span class="c-frame">│</span> <span class="c-agent">BudgetGoalAgent</span>  <span class="c-frame">│</span>      <span class="c-frame">│</span>   <span class="c-agent">GeneralAgent</span>   <span class="c-frame">│</span>                     <span class="c-frame">│</span>
<span class="c-frame">│</span>                     <span class="c-frame">│</span> • <span class="c-sub">Metas poupança</span> <span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">Conceitos Selic</span><span class="c-frame">│</span>                     <span class="c-frame">│</span>
<span class="c-frame">│</span>                     <span class="c-frame">│</span> • <span class="c-sub">Prazos & plano</span> <span class="c-frame">│</span>      <span class="c-frame">│</span> • <span class="c-sub">MathTool (exato)</span><span class="c-frame">│</span>                    <span class="c-frame">│</span>
<span class="c-frame">│</span>                     <span class="c-frame">└────────┬─────────┘</span>      <span class="c-frame">└────────┬─────────┘</span>                     <span class="c-frame">│</span>
<span class="c-frame">└──────────────────────────────┼─────────────────────────┼───────────────────────────────┘</span>
                               <span class="c-frame">│</span>                         <span class="c-frame">│</span>
                 <span class="c-frame">┌─────────────┴───────────┐</span>             <span class="c-frame">│</span>
                 <span class="c-arrow">▼</span>                         <span class="c-arrow">▼</span>             <span class="c-arrow">▼</span>
       <span class="c-frame">┌───────────────────┐</span>     <span class="c-frame">┌───────────────────────────────────┐</span>
       <span class="c-frame">│</span>   <span class="c-data">Google Sheets</span>   <span class="c-frame">│</span>     <span class="c-frame">│</span>          <span class="c-llm">OpenRouter LLM</span>           <span class="c-frame">│</span>
       <span class="c-frame">│</span>   • <span class="c-sub">Persistência</span>  <span class="c-frame">│</span>     <span class="c-frame">│</span>   • <span class="c-sub">Modelo Ling 3.0 Flash Fin</span>     <span class="c-frame">│</span>
       <span class="c-frame">│</span>   • <span class="c-sub">Cache TTL 30s</span> <span class="c-frame">│</span>     <span class="c-frame">│</span>   • <span class="c-sub">Failover em cascata</span>          <span class="c-frame">│</span>
       <span class="c-frame">│</span>   • <span class="c-sub">Extrato real</span>  <span class="c-frame">│</span>     <span class="c-frame">│</span>   • <span class="c-sub">Base local offline</span>            <span class="c-frame">│</span>
       <span class="c-frame">└───────────────────┘</span>     <span class="c-frame">└───────────────────────────────────┘</span>
      </pre>

      <div class="terminal-footer">
        <div>
          <span style="color: #7ee787">✓</span> Arquitetura carregada: <span style="color: #f0f6fc; font-weight: 600;">5 agentes especialistas registrados</span>
        </div>
        <div>
          <span class="prompt-user">nathan@mac</span> <span style="color: #8b949e">❯</span><span class="cursor"></span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

async def main():
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    banner_png = assets_dir / "banner.png"
    arquitetura_png = assets_dir / "arquitetura.png"

    print("Renderizando banner e arquitetura via Playwright Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # 1. Renderizar Banner
        context = await browser.new_context(
            viewport={"width": 1264, "height": 780},
            device_scale_factor=2
        )
        page = await context.new_page()
        await page.set_content(HTML_BANNER, wait_until="networkidle")
        await asyncio.sleep(1)
        container = page.locator(".banner-container")
        await container.screenshot(path=str(banner_png))
        print(f"Banner renderizado em: {banner_png}")
        await context.close()

        # 2. Renderizar Arquitetura
        context2 = await browser.new_context(
            viewport={"width": 1180, "height": 880},
            device_scale_factor=2
        )
        page2 = await context2.new_page()
        await page2.set_content(HTML_ARQUITETURA, wait_until="networkidle")
        await asyncio.sleep(1)
        container2 = page2.locator(".terminal-window")
        await container2.screenshot(path=str(arquitetura_png))
        print(f"Arquitetura renderizada em: {arquitetura_png}")
        await context2.close()

        await browser.close()

    print("Ativos visuais minimalistas gerados com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
