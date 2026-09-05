# Feature 9c01 — Adequação ao Design System (Requisito Mobile-First)

## Contexto e Objetivo
Adequar a interface do chat em Streamlit (`src/app.py`) às diretrizes descritas em `.agents/rules/design-system.md`, com foco no requisito **Mobile-First**:
1. Responsividade total em dispositivos móveis (smartphones e tablets).
2. Botões, cards e gráficos expandidos para 100% da largura do container (`use_container_width=True`).
3. Estilização alinhada aos tokens de cor, tipografia Montserrat e cantos arredondados do Design System.

## Diretrizes Aplicadas
- **Tokens de Cor & Fonte**: Fonte 'Montserrat' via Google Fonts, background `--panel` (#f6f8fb), destaque `--primary` (#2563eb).
- **Mobile-First Layout**:
  - `st.button` com `use_container_width=True`.
  - `st.bar_chart` com `use_container_width=True`.
  - Empilhamento fluido de colunas no mobile.
- **Acessibilidade**: Contraste alto e elementos focáveis.

## Critérios de Aceite
- [ ] A interface aplica os estilos e fonte Montserrat do Design System.
- [ ] Todos os botões e gráficos ajustam-se dinamicamente a 100% da largura em telas móveis sem barras de rolagem horizontais.
- [ ] Suíte de testes unitários 100% aprovada via `uv run pytest`.
