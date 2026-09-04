import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path para o Streamlit reconhecer o pacote 'src'
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
from src.guardrail.validator import GuardrailValidator
from src.agent.engine import FinancialAgent

st.set_page_config(
    page_title="Agente Financeiro IA",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Agente Financeiro Inteligente")
st.caption("Gerenciamento de despesas fixas, receitas, saldos e cálculos numéricos via chat.")

# Inicializa Guardrail e Agente
@st.cache_resource
def get_components():
    return GuardrailValidator(), FinancialAgent()

validator, agent = get_components()

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou seu assistente financeiro. Como posso ajudar com suas despesas fixas, receitas ou cálculos hoje?"
        }
    ]

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if user_input := st.chat_input("Digite sua solicitação (ex: Divida por 2 a conta de aluguel ou Consulte o saldo)..."):
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
            with st.spinner("Processando com o Agente Financeiro..."):
                response = agent.process_message(user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
