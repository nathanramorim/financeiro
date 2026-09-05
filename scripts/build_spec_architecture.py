import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Arquitetura · Financeiro</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0d0f14;
      --box: #12151c;
      --border: #1f2430;
      --text: #e8eaf0;
      --text-sec: #9aa3b5;
      --detail: #6b7386;
      --blue: #4f8ef7;
      --cyan: #3ecfcf;
      --green: #4fd08a;
      --amber: #e8b34f;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Montserrat', sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .container {
      width: 100%;
      max-width: 920px;
      display: flex;
      flex-direction: column;
      gap: 56px;
    }

    header.doc-header {
      border-bottom: 1px solid var(--border);
      padding-bottom: 24px;
    }
    .doc-eyebrow {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--blue);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }
    .doc-header h1 {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: var(--text);
      margin-bottom: 6px;
    }
    .doc-header p {
      font-size: 14px;
      color: var(--text-sec);
    }

    section.view-section {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .section-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--text);
    }
    .section-sub {
      font-size: 13px;
      color: var(--text-sec);
      margin-bottom: 4px;
    }

    .svg-wrapper {
      background: var(--box);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 12px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }
    svg {
      display: block;
      width: 100%;
      height: auto;
    }

    .caption {
      font-size: 11.5px;
      color: var(--detail);
      font-style: italic;
      margin-top: 6px;
      text-align: right;
    }

    /* Legenda */
    footer.legend-section {
      background: var(--box);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .legend-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--detail);
    }
    .legend-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 14px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12.5px;
      color: var(--text-sec);
    }
    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="doc-header">
      <div class="doc-eyebrow">Arquitetura de Software · financeiro</div>
      <h1>Topologia e Fluxo da Malha Multiagente</h1>
      <p>Representação visual da arquitetura e do trajeto de execução de perguntas financeiras</p>
    </header>

    <!-- VISÃO 1 -->
    <section class="view-section">
      <h2 class="section-title">1 · O mapa das peças</h2>
      <p class="section-sub">Estrutura de componentes, fronteira da aplicação e canais de integração externa</p>
      <div class="svg-wrapper">
        <svg viewBox="0 0 860 520" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrow" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#4f8ef7" />
            </marker>
            <marker id="arrow-amber" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#e8b34f" />
            </marker>
            <marker id="arrow-green" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#4fd08a" />
            </marker>
            <marker id="arrow-cyan" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#3ecfcf" />
            </marker>
          </defs>

          <!-- Títulos das Faixas Verticais -->
          <text x="75" y="42" fill="#6b7386" font-size="11" font-family="'JetBrains Mono', monospace" text-anchor="middle">ATOR</text>
          <text x="248" y="42" fill="#6b7386" font-size="11" font-family="'JetBrains Mono', monospace" text-anchor="middle">CLIENTE</text>
          <text x="502" y="42" fill="#6b7386" font-size="11" font-family="'JetBrains Mono', monospace" text-anchor="middle">SISTEMA FINANCEIRO</text>
          <text x="752" y="42" fill="#6b7386" font-size="11" font-family="'JetBrains Mono', monospace" text-anchor="middle">SERVIÇOS EXTERNOS</text>

          <!-- Fronteira do Sistema (390 a 614) -->
          <rect x="390" y="65" width="224" height="425" rx="8" fill="none" stroke="#1f2430" stroke-width="1.5" stroke-dasharray="4 4" />
          <text x="404" y="85" fill="#6b7386" font-size="10" font-family="'JetBrains Mono', monospace">FastAPI :8000</text>

          <!-- 1. ATOR (16 a 134, y=115 h=70, centro y=150) -->
          <rect x="16" y="115" width="118" height="70" rx="8" fill="#12151c" stroke="#1f2430" stroke-width="1.5" />
          <text x="75" y="146" fill="#e8eaf0" font-size="13" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Você</text>
          <text x="75" y="166" fill="#9aa3b5" font-size="11" font-family="'Montserrat', sans-serif" text-anchor="middle">Pessoa usuária</text>

          <!-- 2. CLIENTE (176 a 320, y=115 h=70, centro y=150) -->
          <rect x="176" y="115" width="144" height="70" rx="8" fill="#12151c" stroke="#1f2430" stroke-width="1.5" />
          <text x="248" y="144" fill="#e8eaf0" font-size="13" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Interface Web</text>
          <text x="248" y="162" fill="#9aa3b5" font-size="11" font-family="'Montserrat', sans-serif" text-anchor="middle">Chat e gráficos</text>
          <text x="248" y="177" fill="#6b7386" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">Next.js :3020</text>

          <!-- 3. SISTEMA - CAIXA 1: Porteiro (Guardrail) em x=404 w=196 y=115 h=70 (centro y=150) -->
          <rect x="404" y="115" width="196" height="70" rx="8" fill="#12151c" stroke="#e8b34f" stroke-width="1.5" />
          <text x="502" y="144" fill="#e8eaf0" font-size="13" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Porteiro do assunto</text>
          <text x="502" y="162" fill="#9aa3b5" font-size="11" font-family="'Montserrat', sans-serif" text-anchor="middle">Filtra e barra desvios</text>
          <text x="502" y="177" fill="#e8b34f" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">GuardrailValidator</text>

          <!-- 4. SISTEMA - CAIXA 2: Maestro (AgentRouter) em x=404 w=196 y=219 h=70 (gap=34) -->
          <!-- PROTAGONISTA DO DIAGRAMA (Azul #4f8ef7) -->
          <rect x="404" y="219" width="196" height="70" rx="8" fill="#12151c" stroke="#4f8ef7" stroke-width="2" />
          <text x="502" y="248" fill="#e8eaf0" font-size="13" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Maestro dos agentes</text>
          <text x="502" y="266" fill="#9aa3b5" font-size="11" font-family="'Montserrat', sans-serif" text-anchor="middle">Escolhe o especialista</text>
          <text x="502" y="281" fill="#4f8ef7" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">AgentRouter</text>

          <!-- 5. SISTEMA - CAIXA 3: Equipe Especialista em x=404 w=196 y=323 h=135 (gap=34) -->
          <rect x="404" y="323" width="196" height="135" rx="8" fill="#12151c" stroke="#1f2430" stroke-width="1.5" />
          <text x="502" y="345" fill="#e8eaf0" font-size="12" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Equipe especialista</text>
          <text x="418" y="368" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">• Transações e extrato</text>
          <text x="418" y="386" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">• Relatório e balanço</text>
          <text x="418" y="404" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">• Consultoria 50/30/20</text>
          <text x="418" y="422" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">• Metas de poupança</text>
          <text x="418" y="440" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">• Dúvidas e conceitos</text>

          <!-- 6. EXTERNO 1: Planilha de Dados (660 a 845, y=323 h=60) -->
          <rect x="660" y="323" width="185" height="60" rx="8" fill="#12151c" stroke="#3ecfcf" stroke-width="1.5" />
          <text x="752" y="347" fill="#e8eaf0" font-size="12.5" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Planilha de dados</text>
          <text x="752" y="364" fill="#9aa3b5" font-size="10.5" font-family="'Montserrat', sans-serif" text-anchor="middle">Persistência real</text>
          <text x="752" y="377" fill="#3ecfcf" font-size="8.5" font-family="'JetBrains Mono', monospace" text-anchor="middle">Google Sheets · TTL 30s</text>

          <!-- 7. EXTERNO 2: Inteligência de Texto (660 a 845, y=398 h=60) -->
          <rect x="660" y="398" width="185" height="60" rx="8" fill="#12151c" stroke="#3ecfcf" stroke-width="1.5" />
          <text x="752" y="422" fill="#e8eaf0" font-size="12.5" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Inteligência de texto</text>
          <text x="752" y="439" fill="#9aa3b5" font-size="10.5" font-family="'Montserrat', sans-serif" text-anchor="middle">Geração e cálculos</text>
          <text x="752" y="452" fill="#3ecfcf" font-size="8.5" font-family="'JetBrains Mono', monospace" text-anchor="middle">OpenRouter · Ling 3.0</text>

          <!-- SETAS ORTOGONAIS DO DIAGRAMA 1 -->
          <!-- 1 · Envia pergunta (Ator -> Cliente, y=150) -->
          <path d="M 134 150 L 167 150" stroke="#4f8ef7" stroke-width="1.5" fill="none" marker-end="url(#arrow)" />
          <text x="155" y="141" fill="#9aa3b5" font-size="8.5" font-family="'Montserrat', sans-serif" text-anchor="middle">1 · Digita</text>

          <!-- 2 · Envia mensagem (Cliente -> Porteiro, y=150) -->
          <path d="M 320 150 L 395 150" stroke="#4f8ef7" stroke-width="1.5" fill="none" marker-end="url(#arrow)" />
          <text x="362" y="141" fill="#9aa3b5" font-size="9" font-family="'Montserrat', sans-serif" text-anchor="middle">2 · Posta</text>

          <!-- Recusa imediata (Porteiro -> Cliente, horizontal paralela com 28px de separação em y=122) -->
          <path d="M 404 125 L 329 125" stroke="#e8b34f" stroke-width="1.5" fill="none" marker-end="url(#arrow-amber)" />
          <text x="362" y="117" fill="#e8b34f" font-size="8.5" font-family="'Montserrat', sans-serif" text-anchor="middle">Recusa</text>

          <!-- 3 · Libera assunto (Porteiro -> Maestro, vertical em x=502 de y=185 a y=219) -->
          <path d="M 502 185 L 502 210" stroke="#4f8ef7" stroke-width="1.5" fill="none" marker-end="url(#arrow)" />
          <text x="512" y="204" fill="#9aa3b5" font-size="8.5" font-family="'Montserrat', sans-serif">3 · Aprova</text>

          <!-- 4 · Ativa especialista (Maestro -> Especialistas, vertical em x=502 de y=289 a y=323) -->
          <path d="M 502 289 L 502 314" stroke="#4f8ef7" stroke-width="1.5" fill="none" marker-end="url(#arrow)" />
          <text x="512" y="308" fill="#9aa3b5" font-size="8.5" font-family="'Montserrat', sans-serif">4 · Roteia</text>

          <!-- 5 e 6 · Especialistas <-> Planilha (Ida em y=340, Volta em y=368, separação de 28px) -->
          <path d="M 600 340 L 651 340" stroke="#3ecfcf" stroke-width="1.5" fill="none" marker-end="url(#arrow-cyan)" />
          <text x="630" y="333" fill="#9aa3b5" font-size="8" font-family="'Montserrat', sans-serif" text-anchor="middle">5 · Consulta</text>

          <path d="M 660 368 L 609 368" stroke="#3ecfcf" stroke-width="1.5" fill="none" marker-end="url(#arrow-cyan)" />
          <text x="630" y="361" fill="#9aa3b5" font-size="8" font-family="'Montserrat', sans-serif" text-anchor="middle">6 · Retorna</text>

          <!-- 7 e 8 · Especialistas <-> LLM (Ida em y=415, Volta em y=443, separação de 28px) -->
          <path d="M 600 415 L 651 415" stroke="#3ecfcf" stroke-width="1.5" fill="none" marker-end="url(#arrow-cyan)" />
          <text x="630" y="408" fill="#9aa3b5" font-size="8" font-family="'Montserrat', sans-serif" text-anchor="middle">7 · Pede</text>

          <path d="M 660 443 L 609 443" stroke="#3ecfcf" stroke-width="1.5" fill="none" marker-end="url(#arrow-cyan)" />
          <text x="630" y="436" fill="#9aa3b5" font-size="8" font-family="'Montserrat', sans-serif" text-anchor="middle">8 · Explica</text>

          <!-- Sai da lateral esquerda da caixa dos especialistas (x=404, y=440), desce pelo corredor livre até x=248 e sobe na base da Interface Web (x=248, y=193) -->
          <path d="M 404 440 L 248 440 L 248 193" stroke="#4fd08a" stroke-width="1.5" fill="none" marker-end="url(#arrow-green)" />
          <text x="238" y="310" fill="#4fd08a" font-size="10.5" font-family="'Montserrat', sans-serif" font-weight="600" text-anchor="end">9 · Resposta pronta com cálculos e dados</text>
        </svg>
      </div>
      <div class="caption">Diagrama 1 · Disposição física dos quatro blocos do sistema e conexões ortogonais de serviço</div>
    </section>

    <!-- VISÃO 2 -->
    <section class="view-section">
      <h2 class="section-title">2 · O caminho de uma pergunta</h2>
      <p class="section-sub">Sequência temporal de mensagens com validação de escopo e rota alternativa de recusa</p>
      <div class="svg-wrapper">
        <svg viewBox="0 0 860 510" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="seq-arrow-blue" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#4f8ef7" />
            </marker>
            <marker id="seq-arrow-amber" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#e8b34f" />
            </marker>
            <marker id="seq-arrow-cyan" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#3ecfcf" />
            </marker>
            <marker id="seq-arrow-green" viewBox="0 0 9 9" refX="7.5" refY="4.5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
              <path d="M 0 1.5 L 7.5 4.5 L 0 7.5 z" fill="#4fd08a" />
            </marker>
          </defs>

          <!-- 3 Lifelines Verticais em x=110, 390, 670 -->
          <line x1="110" y1="60" x2="110" y2="480" stroke="#1f2430" stroke-width="1.5" stroke-dasharray="4 4" />
          <line x1="390" y1="60" x2="390" y2="480" stroke="#1f2430" stroke-width="1.5" stroke-dasharray="4 4" />
          <line x1="670" y1="60" x2="670" y2="480" stroke="#1f2430" stroke-width="1.5" stroke-dasharray="4 4" />

          <!-- Cabeçalhos das Lifelines -->
          <rect x="20" y="20" width="180" height="38" rx="6" fill="#12151c" stroke="#1f2430" stroke-width="1.5" />
          <text x="110" y="38" fill="#e8eaf0" font-size="12" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Você · Interface</text>
          <text x="110" y="50" fill="#6b7386" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">Next.js :3020</text>

          <rect x="300" y="20" width="180" height="38" rx="6" fill="#12151c" stroke="#4f8ef7" stroke-width="1.5" />
          <text x="390" y="38" fill="#e8eaf0" font-size="12" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Porteiro & Maestro</text>
          <text x="390" y="50" fill="#4f8ef7" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">FastAPI :8000</text>

          <rect x="580" y="20" width="180" height="38" rx="6" fill="#12151c" stroke="#3ecfcf" stroke-width="1.5" />
          <text x="670" y="38" fill="#e8eaf0" font-size="12" font-family="'Montserrat', sans-serif" font-weight="700" text-anchor="middle">Especialistas & Dados</text>
          <text x="670" y="50" fill="#3ecfcf" font-size="9" font-family="'JetBrains Mono', monospace" text-anchor="middle">Sheets & LLM</text>

          <!-- Caixas de Processamento Centradas nas Lifelines (w=12) -->
          <rect x="104" y="95" width="12" height="360" rx="2" fill="#1f2430" />
          <rect x="384" y="105" width="12" height="340" rx="2" fill="#1f2430" />
          <rect x="664" y="250" width="12" height="135" rx="2" fill="#1f2430" />

          <!-- EVENTO 1 (y=115): Seta horizontal x=110 a x=382 (8px antes de 390) -->
          <line x1="110" y1="115" x2="382" y2="115" stroke="#4f8ef7" stroke-width="1.5" marker-end="url(#seq-arrow-blue)" />
          <text x="246" y="106" fill="#e8eaf0" font-size="11" font-family="'Montserrat', sans-serif" font-weight="600" text-anchor="middle">1 · Envia pergunta financeira ou geral</text>

          <!-- EVENTO 2 (y=167, ritmo vertical 52px): Rota de Recusa em Âmbar #e8b34f -->
          <!-- Seta termina 8px antes da lifeline alvo (x=118) -->
          <line x1="390" y1="167" x2="118" y2="167" stroke="#e8b34f" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#seq-arrow-amber)" />
          <text x="254" y="158" fill="#e8b34f" font-size="10.5" font-family="'Montserrat', sans-serif" font-weight="600" text-anchor="middle">[Se não for finanças] Recusa educada e segura</text>

          <!-- EVENTO 3 (y=219, ritmo vertical 52px): Auto-processamento do Maestro -->
          <path d="M 390 205 L 416 205 L 416 225 L 396 225" stroke="#4f8ef7" stroke-width="1.5" fill="none" marker-end="url(#seq-arrow-blue)" />
          <text x="424" y="218" fill="#9aa3b5" font-size="10" font-family="'Montserrat', sans-serif">2 · Avalia afinidade e escolhe especialista</text>

          <!-- EVENTO 4 (y=271, ritmo vertical 52px): Aciona Especialista x=390 a x=662 -->
          <line x1="390" y1="271" x2="662" y2="271" stroke="#4f8ef7" stroke-width="1.5" marker-end="url(#seq-arrow-blue)" />
          <text x="526" y="262" fill="#e8eaf0" font-size="11" font-family="'Montserrat', sans-serif" font-weight="600" text-anchor="middle">3 · Despacha tarefa para especialista ideal</text>

          <!-- EVENTO 5 (y=323, ritmo vertical 52px): Auto-chamada na base externa -->
          <path d="M 670 310 L 696 310 L 696 330 L 676 330" stroke="#3ecfcf" stroke-width="1.5" fill="none" marker-end="url(#seq-arrow-cyan)" />
          <text x="704" y="323" fill="#3ecfcf" font-size="10" font-family="'Montserrat', sans-serif">4 · Consulta Sheets e LLM</text>

          <!-- EVENTO 6 (y=375, ritmo vertical 52px): Retorno do Especialista x=670 a x=398 -->
          <line x1="670" y1="375" x2="398" y2="375" stroke="#3ecfcf" stroke-width="1.5" marker-end="url(#seq-arrow-cyan)" />
          <text x="534" y="366" fill="#9aa3b5" font-size="10.5" font-family="'Montserrat', sans-serif" font-weight="500" text-anchor="middle">5 · Devolve dados e cálculos conferidos</text>

          <!-- EVENTO 7 (y=427, ritmo vertical 52px): Resposta de Sucesso x=390 a x=118 (Verde #4fd08a) -->
          <line x1="390" y1="427" x2="118" y2="427" stroke="#4fd08a" stroke-width="1.5" marker-end="url(#seq-arrow-green)" />
          <text x="254" y="418" fill="#4fd08a" font-size="11" font-family="'Montserrat', sans-serif" font-weight="600" text-anchor="middle">6 · Exibe resposta formatada com gráficos no chat</text>
        </svg>
      </div>
      <div class="caption">Diagrama 2 · Ordem cronológica de mensagens entre os três papéis com retorno de recusa e sucesso</div>
    </section>

    <!-- LEGENDA DAS CINCO CORES -->
    <footer class="legend-section">
      <div class="legend-title">Legenda de Cores e Semântica Visual</div>
      <div class="legend-grid">
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--blue);"></div>
          <span><strong>Azul (#4f8ef7)</strong> · Fluxo principal e Maestro</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--amber);"></div>
          <span><strong>Âmbar (#e8b34f)</strong> · Porteiro e rota de recusa</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--green);"></div>
          <span><strong>Verde (#4fd08a)</strong> · Resposta bem-sucedida</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--cyan);"></div>
          <span><strong>Ciano (#3ecfcf)</strong> · Serviços externos e dados</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--detail);"></div>
          <span><strong>Cinza (#6b7386)</strong> · Estrutura e anotações técnicas</span>
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
"""

async def main():
    root = Path(__file__).resolve().parent.parent
    docs_dir = root / "docs"
    assets_dir = root / "docs" / "assets"
    docs_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    html_file = docs_dir / "arquitetura.html"
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"Arquivo HTML único gerado em: {html_file}")

    png_file = assets_dir / "arquitetura.png"
    print(f"Renderizando imagem PNG de alta definição em: {png_file}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1020, "height": 1420},
            device_scale_factor=2
        )
        page = await context.new_page()
        await page.goto(f"file://{html_file.resolve()}", wait_until="networkidle")
        await asyncio.sleep(1)

        container = page.locator(".container")
        await container.screenshot(path=str(png_file))
        print(f"Screenshot PNG gerado com sucesso em: {png_file}")
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
