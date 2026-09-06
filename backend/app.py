import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path para o Streamlit reconhecer o pacote 'backend'
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
from backend.guardrail.validator import GuardrailValidator
from backend.agent.engine import FinancialAgent

# Configuração de Página Streamlit
st.set_page_config(
    page_title="Agente Financeiro IA",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Injeção de Fonte Montserrat e Tokens de CSS do Design System (.agents/rules/design-system.md)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
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
        --radius: 12px;
        --radius-sm: 8px;
        --radius-pill: 999px;
        --font: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    html, body, [class*="css"] {
        font-family: var(--font) !important;
        color: var(--text);
    }
    .eyebrow {
        display: inline-flex;
        font-family: var(--font);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: var(--primary);
        background: #eff4ff;
        border: 1px solid var(--panel-border-strong);
        padding: 4px 12px;
        border-radius: var(--radius-pill);
        margin-bottom: 8px;
    }
    .stApp {
        background-color: var(--bg);
    }
    h1 {
        font-family: var(--font) !important;
        font-weight: 900 !important;
        color: var(--text) !important;
        font-size: 1.85rem !important;
        letter-spacing: -0.5px;
    }
    .stCaption {
        font-family: var(--font) !important;
        font-weight: 500 !important;
        color: var(--text-dim) !important;
        font-size: 0.9rem !important;
    }
    .stChatMessage {
        background: var(--panel) !important;
        border: 1px solid var(--panel-border) !important;
        border-radius: var(--radius) !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }
    .stChatMessage:hover {
        border-color: var(--panel-border-strong) !important;
    }
    .stButton button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-family: var(--font) !important;
        transition: all 0.15s ease-in-out !important;
    }
    .stButton button:focus-visible {
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px !important;
    }
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.75rem !important;
        }
        h1 {
            font-size: 1.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">FINANÇAS PESSOAIS</div>', unsafe_allow_html=True)
st.title("💰 Agente Financeiro Inteligente")
st.caption("Gerenciamento de despesas, receitas, saldos e relatórios executivos.")

# Inicializa Guardrail e Agente
validator = GuardrailValidator()
agent = FinancialAgent()

# Inicialização do estado de sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou seu assistente financeiro. Como posso ajudar com suas despesas fixas, receitas ou cálculos hoje?"
        }
    ]

if "pending_transaction" not in st.session_state:
    st.session_state.pending_transaction = None

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if report_data := message.get("report_data"):
            st.divider()
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("⚖️ Receita vs Despesa")
                st.bar_chart({
                    "Receitas": report_data["total_receitas"],
                    "Despesas": report_data["total_despesas"]
                }, use_container_width=True)
            with col2:
                st.subheader("🏷️ Despesas por Categoria")
                if report_data.get("despesas_por_categoria"):
                    st.bar_chart(report_data["despesas_por_categoria"], use_container_width=True)
                else:
                    st.info("Nenhuma despesa para exibir no gráfico.")

# Exibe os botões de confirmação se houver uma transação pendente (Mobile-First: 100% width)
if st.session_state.pending_transaction:
    tx = st.session_state.pending_transaction
    st.info(
        f"### ⚠️ Confirmação Solicitada\n"
        f"- **Ação:** {tx['action_label']}\n"
        f"- **Descrição:** {tx['descricao']}\n"
        f"- **Valor:** R$ {tx['valor']:.2f}"
        + (f"\n- **Categoria:** {tx.get('categoria')}" if tx.get('categoria') else "")
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Confirmar Transação", key="confirm_btn", type="primary", use_container_width=True):
            response = agent.execute_transaction(tx)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.pending_transaction = None
            st.rerun()
    with col2:
        if st.button("❌ Cancelar", key="cancel_btn", use_container_width=True):
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Operação de **{tx['action_label']}** cancelada pelo usuário."})
            st.session_state.pending_transaction = None
            st.rerun()

# Input do usuário
if user_input := st.chat_input("Digite sua solicitação (ex: relatorio, add despesa Mercado 150 ou consulte o saldo)..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Validação de Guardrail
    guard_res = validator.validate(user_input)

    with st.chat_message("assistant"):
        if not guard_res.is_valid:
            st.error(guard_res.message)
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {guard_res.message}"})
        else:
            # 2. Verifica se a mensagem exige confirmação de mutação
            pending_tx = agent.detect_mutation_intent(user_input)
            if pending_tx:
                st.session_state.pending_transaction = pending_tx
                confirm_msg = f"📋 **{pending_tx['action_label']} identificada.** Por favor, confirme a alteração usando os botões de ação."
                st.markdown(confirm_msg)
                st.session_state.messages.append({"role": "assistant", "content": confirm_msg})
                st.rerun()
            else:
                spinner_msg = "📊 Gerando relatório financeiro e consolidando gráficos..." if agent.is_report_request(user_input) else "Processando com o Agente Financeiro..."
                with st.spinner(spinner_msg):
                    response = agent.process_message(user_input)
                    st.markdown(response)
                    msg_obj = {"role": "assistant", "content": response}
                    if agent.is_report_request(user_input):
                        report_data = agent.generate_report_data()
                        msg_obj["report_data"] = report_data
                        st.divider()
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.subheader("⚖️ Receita vs Despesa")
                            st.bar_chart({
                                "Receitas": report_data["total_receitas"],
                                "Despesas": report_data["total_despesas"]
                            }, use_container_width=True)
                        with col2:
                            st.subheader("🏷️ Despesas por Categoria")
                            if report_data.get("despesas_por_categoria"):
                                st.bar_chart(report_data["despesas_por_categoria"], use_container_width=True)
                            else:
                                st.info("Nenhuma despesa para exibir no gráfico.")
                    st.session_state.messages.append(msg_obj)


