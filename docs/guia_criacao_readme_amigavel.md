# 📘 Guia Prático: Como Criar READMEs Atraentes, Amigáveis e com Arquitetura no Estilo Claude Code

Este guia documenta o padrão, as técnicas e as ferramentas utilizadas para construir um **README de alto impacto** para projetos de software e inteligência artificial — mantendo um tom amigável, acolhedor, visualmente integrado ao Design System do projeto e com diagramas de arquitetura simples e elegantes.

---

## 🎯 1. Princípios Fundamentais

1. **Tom Amigável & Acessível:**
   - Explique o projeto como se estivesse conversando com um amigo curioso.
   - Evite abrir o README com parágrafos densos de arquitetura ou siglas herméticas.
   - Apresente primeiro o **valor e a facilidade de uso**, depois o funcionamento interno e, por fim, as instruções técnicas.

2. **Fidelidade ao Design System Real ("Nada de imagens genéricas"):**
   - **Evite:** Ilustrações genéricas de banco de imagens, personagens 3D cartunescos ou artes conceituais que não refletem a tela real do app.
   - **Prefira:** Mockups e banners compostos pelos **próprios componentes do produto** (stat tiles, cards com bordas suaves, cores oficiais do Design System, tipografia real e gráficos minimalistas).

3. **Arquitetura Simples e Direta (Estilo Claude Code):**
   - O estilo característico do Claude Code utiliza **desenhos em texto puro (ASCII / Unicode Box Drawing)**.
   - São leves, legíveis em qualquer tela, funcionam perfeitamente no terminal e renderizam instantaneamente no GitHub sem quebrar.

4. **Demonstração Viva ("Show, Don't Just Tell"):**
   - Um GIF animado de 10 a 20 segundos gravado automaticamente via Playwright demonstra o fluxo real do produto melhor do que 10 parágrafos de texto.

---

## 📐 2. Estrutura Anatômica do README

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BANNER & IDENTIDADE VISUAL (Design System)               │
│    • Imagem de topo 16:9 limpa e moderna                    │
│    • Badges de status (Stack, Testes, Licença)              │
├─────────────────────────────────────────────────────────────┤
│ 2. O QUE É O PROJETO (Em 3 tópicos amigáveis)              │
│    • Benefício direto para o usuário                         │
├─────────────────────────────────────────────────────────────┤
│ 3. DEMONSTRAÇÃO EM AÇÃO (GIF Playwright)                    │
│    • Gravação do app funcionando (chat, cliques, gráficos)  │
├─────────────────────────────────────────────────────────────┤
│ 4. EQUIPE / ESPECIALISTAS (Tabela Humanizada)               │
│    • Quem é cada agente/módulo + perguntas de exemplo       │
├─────────────────────────────────────────────────────────────┤
│ 5. ARQUITETURA NO ESTILO CLAUDE CODE (ASCII + Explicação)   │
│    • Diagrama box-drawing simples em bloco ```text          │
│    • O ciclo da informação em 4 passos simples              │
├─────────────────────────────────────────────────────────────┤
│ 6. COMO EXECUTAR (Rápido e sem mistério)                    │
│    • Pré-requisitos objetivos                               │
│    • Comando único (ex: ./scripts/dev.sh)                   │
├─────────────────────────────────────────────────────────────┤
│ 7. TESTES & DOCUMENTAÇÃO TÉCNICA APROFUNDADA                │
│    • Comandos de testes e links para docs/                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 3. Como Desenhar Arquiteturas no Estilo Claude Code

O Claude Code projeta fluxos usando a família de caracteres Unicode **Box Drawing**. Eles garantem cantos retos e alinhamento perfeito em fontes monoespaçadas.

### Conjunto de Caracteres Essenciais:
- Cantos: `┌` `┐` `└` `┘`
- Retas: `─` `│`
- Junções: `├` `┤` `┬` `┴` `┼`
- Setas de direção: `▼` `▲` `►` `◄` `➔` `•`

### Exemplo de Diagrama de Camadas:
```text
┌────────────────────────────────────────────────────────┐
│                   USUÁRIO / BROWSER                    │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP / JSON (:3020)
                            ▼
┌────────────────────────────────────────────────────────┐
│             FRONTEND (Next.js 15 — :3020)              │
│   • Interface Mobile-First   • ChatContainer           │
│   • Sugestões de Input       • Gráficos SVG Nativos    │
└───────────────────────────┬────────────────────────────┘
                            │ REST POST /api/chat (:8000)
                            ▼
┌────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI — :8000)                │
│                                                        │
│   ┌────────────────────────────────────────────────┐   │
│   │              GUARDRAIL VALIDATOR               │   │
│   │   • Validação de escopo estrito                │   │
│   └───────────────────────┬────────────────────────┘   │
│                           │ Mensagem Aprovada          │
│                           ▼                            │
│   ┌────────────────────────────────────────────────┐   │
│   │                 AGENT ROUTER                   │   │
│   │   • Despacho por afinidade para especialistas  │   │
│   └───────────────────────┬────────────────────────┘   │
│                           │                            │
│           ┌───────────────┼───────────────┐            │
│           ▼               ▼               ▼            │
│     ┌───────────┐   ┌───────────┐   ┌───────────┐      │
│     │Transaction│   │  Report   │   │ Advisory  │      │
│     │   Agent   │   │   Agent   │   │   Agent   │      │
│     └─────┬─────┘   └─────┬─────┘   └─────┬─────┘      │
└───────────┼───────────────┼───────────────┼────────────┘
            │               │               │
            ▼               ▼               ▼
   ┌──────────────────────────────────────────────┐
   │            SERVIÇOS & INTEGRAÇÕES            │
   │  • Google Sheets API     • OpenRouter LLM    │
   └──────────────────────────────────────────────┘
```

> **Dica de Ouro:** Para transformar esse diagrama em imagem PNG de alta definição para redes sociais ou preview do GitHub, renderize o bloco `<pre>` dentro de uma moldura de terminal macOS com fundo escuro (`#0f172a`), tipografia `JetBrains Mono` e tire screenshot via Playwright Chromium.

---

## 🎬 4. Como Gravar o GIF Automatizado com Playwright

Evite gravar a tela manualmente (o arquivo fica pesado, tremido ou com resoluções desiguais). Use um script Python ou Node.js com Playwright:

### Script de Automação (`scripts/record_demo.py`):
```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess

async def record_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir="scripts/videos/",
            record_video_size={"width": 1080, "height": 720},
            viewport={"width": 1080, "height": 720},
            device_scale_factor=2,
        )
        page = await context.new_page()

        # 1. Acessa a aplicação local
        await page.goto("http://localhost:3020", wait_until="networkidle")
        await asyncio.sleep(1.5)

        # 2. Interage com botões de sugestão
        btn = page.locator("button:has-text('Taxa Selic')").first
        if await btn.is_visible():
            await btn.hover()
            await asyncio.sleep(0.6)
            await btn.click()
            await asyncio.sleep(1.0)
            await page.locator("button:has-text('Enviar')").first.click()
            await asyncio.sleep(3.5)

        await context.close()
        await browser.close()

    # 3. Converte para GIF otimizado com palettegen via ffmpeg
    subprocess.run([
        "ffmpeg", "-y", "-i", "scripts/videos/video_gerado.webm",
        "-vf", "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "docs/assets/demo.gif"
    ], check=True)

if __name__ == "__main__":
    asyncio.run(record_chat())
```

**Por que essa pipeline com ffmpeg é superior?**
- `palettegen` analisa todas as cores do vídeo e cria uma paleta personalizada de 256 cores.
- `paletteuse` aplica essa paleta com dithering, gerando um GIF sem granulação e com menos de 3.5 MB.

---

## 🎨 5. Como Criar o Banner Baseado no Design System

Para manter total coerência estética:
1. Abra o arquivo de regras de design do seu projeto (ex: `.agents/rules/design-system.md`).
2. Identifique as variáveis de cores (`--primary`, `--panel`, `--text`, `--success`, etc.).
3. Monte uma página HTML estática contendo:
   - Eyebrow em pílula (ex: `⚡ ARQUITETURA MULTIAGENTE`).
   - Título principal com peso 900 na fonte oficial do projeto (ex: *Montserrat*).
   - 3 **Stat Tiles** reais com números de exemplo (`Saldo Líquido`, `Receitas`, `Despesas`).
   - Cards com divisões reais (`Gráfico de Barras` e `Balão de Chat`).
4. Fotografe via Playwright com `device_scale_factor=2` para exportar um PNG nítido e responsivo.

---

## 📝 6. Template Pronto de README para Copiar e Colar

```markdown
<div align="center">

<img src="docs/assets/banner.png" alt="Banner do Projeto" width="100%" />

# 🚀 Nome do Projeto

**Subtítulo amigável em uma frase explicando o que o app faz.**  
Um parágrafo acolhedor explicando como o projeto ajuda a pessoa usuária no dia a dia.

[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20Next.js-blue?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)

</div>

---

## ✨ O que você pode fazer por aqui?

1. **Funcionalidade 1:** Explicação simples em português direto.
2. **Funcionalidade 2:** Sem jargões técnicos ou complicações.
3. **Funcionalidade 3:** Foco no benefício real para quem usa.

---

## 🎬 Veja em Ação

<div align="center">
  <img src="docs/assets/demo.gif" alt="Demonstração" width="100%" />
</div>

---

## 🏛️ Arquitetura do Sistema

```text
[COLE AQUI SEU DIAGRAMA ASCII NO ESTILO CLAUDE CODE]
```

### O fluxo em 4 passos simples:
1. **Passo 1:** O usuário realiza uma ação na interface.
2. **Passo 2:** O Gateway valida as regras de segurança e escopo.
3. **Passo 3:** O Roteador seleciona o especialista correto.
4. **Passo 4:** A resposta é calculada e persistida nos dados reais.

---

## 🚀 Como Rodar Localmente

```bash
# 1. Clonar e configurar
git clone https://github.com/usuario/repositorio.git
cd repositorio
cp .env.example .env

# 2. Iniciar aplicação
./scripts/dev.sh
```

---

## 🧪 Testes Automatizados

```bash
uv run pytest
```
```

---

## 💡 Resumo do Checklist para um README Nota 10

- [ ] O tom inicial parece uma conversa amigável e acessível?
- [ ] Há um banner limpo baseado no Design System (sem personagens ou 3D desconexos)?
- [ ] Há um GIF demonstrando o fluxo em tempo real?
- [ ] O diagrama de arquitetura está claro, simples e em formato ASCII estilo Claude Code?
- [ ] Há um comando rápido para quem acabou de clonar rodar sem atrito?
- [ ] Chaves de API e credenciais foram omitidas e protegidas por `.env.example`?
