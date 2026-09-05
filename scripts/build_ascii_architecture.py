import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import html

DIAGRAM_TEXT = """┌────────────────────────────────────────────────────────────────────────┐
│                          USUÁRIO / NAVEGADOR                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (:3020)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js 15 — :3020)                      │
│   • Interface Mobile-First          • Renderização Markdown & Badges   │
│   • Chips de Sugestões Rápidas      • Gráficos Determinísticos SVG     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST POST /api/chat (:8000)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI — :8000)                         │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                    GUARDRAIL VALIDATOR                         │   │
│   │   • Validação de escopo estritamente financeiro                │   │
│   │   • Bloqueio de injeções de prompt e assuntos fora de contexto │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
│                                   │ Mensagem Aprovada                  │
│                                   ▼                                    │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                       AGENT ROUTER                             │   │
│   │   • Analisa a intenção e calcula afinidade de cada especialista│   │
│   │   • Despacha para o especialista com maior score (BaseAgent)   │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
│                                   │                                    │
│               ┌───────────────────┼───────────────────┐                │
│               ▼                   ▼                   ▼                │
│      ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│      │TransactionAgent │ │   ReportAgent   │ │  AdvisoryAgent  │       │
│      │ • Entradas/Saídas │ • Balanço geral │ │ • Regra 50/30/20│       │
│      │ • Categorização │ │ • Gráficos SVG  │ │ • Consultoria   │       │
│      └────────┬────────┘ └────────┬────────┘ └────────┬────────┘       │
│               │                   │                   │                │
│               └─────────┬─────────┴─────────┬─────────┘                │
│                         ▼                   ▼                          │
│                ┌─────────────────┐ ┌─────────────────┐                 │
│                │ BudgetGoalAgent │ │  GeneralAgent   │                 │
│                │ • Metas poupança│ │ • Conceitos     │                 │
│                │ • Prazos & plano│ │ • MathTool      │                 │
│                └────────┬────────┘ └────────┬────────┘                 │
└─────────────────────────┼───────────────────┼──────────────────────────┘
                          │                   │
             ┌────────────┴─────────┐         │
             ▼                      ▼         ▼
    ┌──────────────────┐   ┌───────────────────────────┐
    │  Google Sheets   │   │      OpenRouter LLM       │
    │  • Persistência  │   │  • Modelo Ling Flash Fin  │
    │  • Cache TTL 30s │   │  • Failover em cascata    │
    │  • Extrato real  │   │  • Base local offline     │
    └──────────────────┘   └───────────────────────────┘"""

def colorize_ascii(text: str) -> str:
    lines = text.split("\n")
    colored_lines = []
    
    for line in lines:
        escaped = html.escape(line)
        
        replacements = [
            ("USUÁRIO / NAVEGADOR", '<span class="tok-user">USUÁRIO / NAVEGADOR</span>'),
            ("FRONTEND (Next.js 15 — :3020)", '<span class="tok-frontend">FRONTEND (Next.js 15 — :3020)</span>'),
            ("BACKEND (FastAPI — :8000)", '<span class="tok-backend">BACKEND (FastAPI — :8000)</span>'),
            ("GUARDRAIL VALIDATOR", '<span class="tok-guardrail">GUARDRAIL VALIDATOR</span>'),
            ("AGENT ROUTER", '<span class="tok-router">AGENT ROUTER</span>'),
            ("TransactionAgent", '<span class="tok-agent">TransactionAgent</span>'),
            ("ReportAgent", '<span class="tok-agent">ReportAgent</span>'),
            ("AdvisoryAgent", '<span class="tok-agent">AdvisoryAgent</span>'),
            ("BudgetGoalAgent", '<span class="tok-agent">BudgetGoalAgent</span>'),
            ("GeneralAgent", '<span class="tok-agent">GeneralAgent</span>'),
            ("Google Sheets", '<span class="tok-sheets">Google Sheets</span>'),
            ("OpenRouter LLM", '<span class="tok-llm">OpenRouter LLM</span>'),
            ("HTTP / JSON (:3020)", '<span class="tok-proto">HTTP / JSON (:3020)</span>'),
            ("REST POST /api/chat (:8000)", '<span class="tok-proto">REST POST /api/chat (:8000)</span>'),
            ("Mensagem Aprovada", '<span class="tok-approved">Mensagem Aprovada</span>'),
            ("•", '<span class="tok-bullet">•</span>'),
            ("▼", '<span class="tok-arrow">▼</span>'),
        ]
        
        for old, new in replacements:
            escaped = escaped.replace(old, new)
            
        colored_lines.append(escaped)
        
    return "\n".join(colored_lines)

HTML_PAGE = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Arquitetura Terminal — Financeiro</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: #0d0f14;
      font-family: Menlo, Monaco, 'SF Mono', Consolas, 'Courier New', monospace;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }}
    .terminal-card {{
      background: #11141d;
      border: 1px solid #232a3b;
      border-radius: 12px;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.05);
      overflow: hidden;
      display: inline-block;
    }}
    .terminal-header {{
      background: #161b26;
      border-bottom: 1px solid #232a3b;
      padding: 14px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .terminal-dots {{
      display: flex;
      gap: 8px;
    }}
    .dot {{
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }}
    .dot.red {{ background: #ff5f56; box-shadow: inset 0 0 0 1px #e0443e; }}
    .dot.yellow {{ background: #ffbd2e; box-shadow: inset 0 0 0 1px #dea123; }}
    .dot.green {{ background: #27c93f; box-shadow: inset 0 0 0 1px #1aab29; }}
    .terminal-title {{
      font-size: 12px;
      color: #9aa3b5;
      letter-spacing: 0.5px;
      font-weight: 500;
    }}
    .terminal-badge {{
      font-size: 11px;
      color: #4f8ef7;
      background: rgba(79, 142, 247, 0.12);
      padding: 3px 10px;
      border-radius: 4px;
      border: 1px solid rgba(79, 142, 247, 0.25);
      font-weight: 500;
    }}
    .terminal-body {{
      padding: 28px 36px 36px 36px;
      background: #0d1017;
    }}
    pre {{
      font-family: Menlo, Monaco, 'SF Mono', Consolas, 'Courier New', monospace;
      font-size: 13.5px;
      line-height: 1.28;
      letter-spacing: 0;
      color: #62728d;
      font-weight: 400;
      white-space: pre;
    }}
    /* Semantic highlighting */
    .tok-user {{ color: #ffffff; }}
    .tok-frontend {{ color: #38bdf8; }}
    .tok-backend {{ color: #a78bfa; }}
    .tok-guardrail {{ color: #fbbf24; }}
    .tok-router {{ color: #60a5fa; }}
    .tok-agent {{ color: #7dd3fc; }}
    .tok-sheets {{ color: #4ade80; }}
    .tok-llm {{ color: #2dd4bf; }}
    .tok-proto {{ color: #38bdf8; }}
    .tok-approved {{ color: #4ade80; }}
    .tok-bullet {{ color: #60a5fa; }}
    .tok-arrow {{ color: #60a5fa; }}
  </style>
</head>
<body>
  <div class="terminal-card">
    <div class="terminal-header">
      <div class="terminal-dots">
        <div class="dot red"></div>
        <div class="dot yellow"></div>
        <div class="dot green"></div>
      </div>
      <div class="terminal-title">financeiro · arquitetura-multiagente.txt</div>
      <div class="terminal-badge">claude-code terminal</div>
    </div>
    <div class="terminal-body">
      <pre><code>{colorize_ascii(DIAGRAM_TEXT)}</code></pre>
    </div>
  </div>
</body>
</html>
"""

async def main():
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = root / "docs" / "arquitetura_terminal.html"
    html_file.write_text(HTML_PAGE, encoding="utf-8")
    print(f"HTML gerado em: {html_file}")
    
    png_file = assets_dir / "arquitetura_terminal.png"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1150, "height": 1350},
            device_scale_factor=2
        )
        page = await context.new_page()
        await page.goto(f"file://{html_file.resolve()}", wait_until="networkidle")
        await asyncio.sleep(0.5)
        
        card = page.locator(".terminal-card")
        await card.screenshot(path=str(png_file))
        print(f"PNG gerado em: {png_file}")
        
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
