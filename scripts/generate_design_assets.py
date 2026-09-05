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
      --success: #16a34a;
      --success-bg: #dcfce7;
      --warning: #d97706;
      --warning-bg: #fef3c7;
      --accent-indigo: #4f46e5;
      --accent-violet: #7c3aed;
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

    .diagram-container {
      width: 1200px;
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: 20px;
      box-shadow: 0 12px 36px rgba(15, 23, 42, 0.06);
      padding: 40px 48px;
    }

    .diagram-header {
      text-align: center;
      margin-bottom: 36px;
    }
    .eyebrow {
      display: inline-flex;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      color: var(--primary);
      background: #eff4ff;
      border: 1px solid var(--panel-border-strong);
      padding: 5px 14px;
      border-radius: var(--radius-pill);
      margin-bottom: 12px;
    }
    .diagram-header h2 {
      font-size: 28px;
      font-weight: 900;
      color: var(--text);
      letter-spacing: -0.6px;
      margin-bottom: 6px;
    }
    .diagram-header p {
      font-size: 15px;
      color: var(--text-dim);
      font-weight: 500;
    }

    /* 4-Stage Horizontal Pipeline */
    .pipeline-grid {
      display: grid;
      grid-template-columns: 240px 40px 240px 40px 330px 40px 210px;
      align-items: center;
    }

    .stage-card {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius);
      padding: 20px;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .stage-card.highlight {
      background: #ffffff;
      border: 1.5px solid var(--primary);
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
    }

    .stage-badge {
      display: inline-flex;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      margin-bottom: 12px;
      align-self: flex-start;
    }
    .stage-badge.blue { background: #eff4ff; color: var(--primary); }
    .stage-badge.green { background: var(--success-bg); color: var(--success); }
    .stage-badge.amber { background: var(--warning-bg); color: var(--warning); }
    .stage-badge.indigo { background: #eef2ff; color: var(--accent-indigo); }

    .stage-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .stage-desc {
      font-size: 12px;
      color: var(--text-dim);
      line-height: 1.5;
      margin-bottom: 14px;
    }

    .stage-footer {
      border-top: 1px solid var(--panel-border);
      padding-top: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--text-dim);
      font-weight: 600;
    }

    /* Arrow Connectors */
    .arrow-col {
      display: flex;
      justify-content: center;
      align-items: center;
      color: var(--panel-border-strong);
      font-size: 24px;
      font-weight: 900;
    }

    /* Specialists Vertical Stack inside Stage 3 */
    .specialists-stack {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .spec-item {
      background: #ffffff;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-sm);
      padding: 9px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
    }
    .spec-name {
      font-weight: 700;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .spec-role {
      font-size: 10px;
      color: var(--text-dim);
      background: var(--panel);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }

    /* Footer Legend */
    .diagram-footer {
      margin-top: 32px;
      padding-top: 20px;
      border-top: 1px solid var(--panel-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-dim);
    }
    .legend-row {
      display: flex;
      gap: 16px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
    }
    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div class="diagram-container">
    <div class="diagram-header">
      <div class="eyebrow">Arquitetura de Ponta a Ponta</div>
      <h2>Fluxo de Execução Multiagente</h2>
      <p>Do clique do usuário no Next.js à persistência determinística no Google Sheets</p>
    </div>

    <div class="pipeline-grid">
      <!-- 1. Frontend -->
      <div class="stage-card">
        <div>
          <span class="stage-badge blue">1. Interface</span>
          <div class="stage-title">📱 Next.js 15</div>
          <div class="stage-desc">
            Dashboard mobile-first com chat interativo, sugestões rápidas, renderização rica em markdown e gráficos SVG nativos.
          </div>
        </div>
        <div class="stage-footer">Porta :3020</div>
      </div>

      <div class="arrow-col">➔</div>

      <!-- 2. API & Segurança -->
      <div class="stage-card">
        <div>
          <span class="stage-badge amber">2. Gateway & Validação</span>
          <div class="stage-title">🛡️ FastAPI + Guardrail</div>
          <div class="stage-desc">
            Endpoints REST desacoplados. O <code>GuardrailValidator</code> filtra injeções e bloqueia tópicos não financeiros antes do processamento.
          </div>
        </div>
        <div class="stage-footer">Porta :8000</div>
      </div>

      <div class="arrow-col">➔</div>

      <!-- 3. Roteamento & Especialistas -->
      <div class="stage-card highlight">
        <div>
          <span class="stage-badge indigo">3. Malha Multiagente</span>
          <div class="stage-title">🧭 AgentRouter</div>
          <div class="stage-desc" style="margin-bottom: 10px;">
            Calcula afinidade e direciona ao agente ideal:
          </div>

          <div class="specialists-stack">
            <div class="spec-item">
              <span class="spec-name">💳 TransactionAgent</span>
              <span class="spec-role">Lançamentos</span>
            </div>
            <div class="spec-item">
              <span class="spec-name">📊 ReportAgent</span>
              <span class="spec-role">Balanço</span>
            </div>
            <div class="spec-item">
              <span class="spec-name">💡 AdvisoryAgent</span>
              <span class="spec-role">Consultoria</span>
            </div>
            <div class="spec-item">
              <span class="spec-name">🎯 BudgetGoalAgent</span>
              <span class="spec-role">Metas</span>
            </div>
            <div class="spec-item">
              <span class="spec-name">📚 GeneralAgent</span>
              <span class="spec-role">Conceitos</span>
            </div>
          </div>
        </div>
        <div class="stage-footer" style="margin-top: 10px;">BaseAgent Plug-and-Play</div>
      </div>

      <div class="arrow-col">➔</div>

      <!-- 4. Dados e LLM -->
      <div class="stage-card">
        <div>
          <span class="stage-badge green">4. Serviços & Dados</span>
          <div class="stage-title">📦 Integrações</div>
          <div class="stage-desc">
            Execução de ferramentas determinísticas (cálculo e persistência real) + inteligência generativa com failover.
          </div>
          <div style="font-size: 12px; line-height: 1.6; color: var(--text); font-weight: 500; margin-top: 6px;">
            • <strong>Google Sheets</strong> (Backup/Cache)<br>
            • <strong>OpenRouter API</strong> (LLM)<br>
            • <strong>MathTool</strong> (Cálculo exato)
          </div>
        </div>
        <div class="stage-footer">gspread + httpx</div>
      </div>
    </div>

    <!-- Rodapé -->
    <div class="diagram-footer">
      <div>Desenvolvido com foco em alta performance, clareza visual e separação estrita de responsabilidades.</div>
      <div class="legend-row">
        <div class="legend-item"><span class="legend-dot" style="background: var(--primary)"></span> Frontend</div>
        <div class="legend-item"><span class="legend-dot" style="background: var(--warning)"></span> Segurança</div>
        <div class="legend-item"><span class="legend-dot" style="background: var(--accent-indigo)"></span> Multiagente</div>
        <div class="legend-item"><span class="legend-dot" style="background: var(--success)"></span> Dados</div>
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
            viewport={"width": 1264, "height": 720},
            device_scale_factor=2
        )
        page2 = await context2.new_page()
        await page2.set_content(HTML_ARQUITETURA, wait_until="networkidle")
        await asyncio.sleep(1)
        container2 = page2.locator(".diagram-container")
        await container2.screenshot(path=str(arquitetura_png))
        print(f"Arquitetura renderizada em: {arquitetura_png}")
        await context2.close()

        await browser.close()

    print("Ativos visuais minimalistas gerados com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
