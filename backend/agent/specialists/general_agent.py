import json
import logging
import requests
from typing import Optional
from backend.agent.base import BaseAgent, AgentContext, AgentResult
from backend.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
from backend.agent.prompts import GENERAL_AGENT_PROMPT
from backend.tools.math_tool import MathTool
from backend.tools.expenses import ExpenseTool

logger = logging.getLogger("GeneralFinancialAgent")

class GeneralFinancialAgent(BaseAgent):
    """Especialista em dúvidas conceituais de finanças, operações matemáticas e fallback resiliente."""

    def __init__(
        self,
        api_key: str = OPENROUTER_API_KEY,
        model: str = OPENROUTER_MODEL,
        expense_tool: Optional[ExpenseTool] = None
    ):
        super().__init__(
            name="general_agent",
            description="Especialista em conceitos financeiros gerais, operações matemáticas e fallback resiliente."
        )
        self.system_prompt = GENERAL_AGENT_PROMPT
        self.api_key = api_key or ""
        self.model = model or "inclusionai/ling-3.0-flash-fin:free"
        self.base_url = OPENROUTER_BASE_URL
        self.expense_tool = expense_tool or ExpenseTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        # Operações matemáticas explícitas
        if any(term in msg_lower for term in [
            "dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por",
            "multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2", "quanto é", "calcule"
        ]):
            return 0.88

        # Conceitos econômicos e financeiros frequentes
        concept_terms = [
            "selic", "cdi", "reserva de emergência", "reserva de emergencia",
            "inflação", "inflacao", "ipca", "juros compostos", "o que é", "como funciona",
            "investir", "investimento", "poupança", "poupanca"
        ]
        if any(term in msg_lower for term in concept_terms):
            return 0.80

        # Fallback baseline para qualquer mensagem financeira
        return 0.30

    def process(self, context: AgentContext) -> AgentResult:
        msg = context.message
        msg_lower = msg.lower()

        # 1. Operações matemáticas determinísticas em despesas fixas
        if any(term in msg_lower for term in ["dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Divididas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_div = MathTool.divide(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_div:.2f}**")
            return AgentResult(
                reply="\n".join(res),
                agent_name=self.name,
                confidence=0.90,
                suggested_actions=["Saldo Atual", "Ver Relatório"]
            )

        if any(term in msg_lower for term in ["multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Multiplicadas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_mult = MathTool.multiply(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_mult:.2f}**")
            return AgentResult(
                reply="\n".join(res),
                agent_name=self.name,
                confidence=0.90,
                suggested_actions=["Saldo Atual", "Ver Relatório"]
            )

        # 2. Tentativa via LLM (OpenRouter) com failover automático de modelos
        if self.api_key and self.api_key != "mock_key":
            llm_result = self._try_llm_completion(msg, context.history)
            if llm_result:
                return AgentResult(
                    reply=llm_result,
                    agent_name=self.name,
                    confidence=0.92,
                    suggested_actions=["Ver Relatório", "Saldo Atual", "Dicas de Economia"]
                )

        # 3. Base de Conhecimento Local (Fallback Determinístico de Alta Qualidade)
        local_concept = self._get_local_concept_explanation(msg_lower)
        if local_concept:
            return AgentResult(
                reply=local_concept,
                agent_name=self.name,
                confidence=0.88,
                suggested_actions=["Ver Relatório", "Saldo Atual", "Dicas de Economia"]
            )

        # 4. Fallback amigável com orientação sobre as capacidades do sistema
        fallback_msg = (
            "Olá! Sou seu assistente financeiro inteligente. Você pode me pedir para:\n"
            "- 💳 **Registrar gastos e ganhos:** *'Gastei 50 no almoço'* ou *'Add receita Salário 5000'*\n"
            "- 📊 **Ver relatórios e gráficos:** *'Relatório'* ou *'Qual meu saldo?'*\n"
            "- 💡 **Receber conselhos orçamentários:** *'Como economizar?'* ou *'Estou gastando muito?'*\n"
            "- 🎯 **Acompanhar metas de economia:** *'Minha meta é juntar R$ 1000'*\n"
            "- 🧠 **Tirar dúvidas conceituais:** *'O que é taxa Selic?'* ou *'O que é CDI?'*"
        )
        return AgentResult(
            reply=fallback_msg,
            agent_name=self.name,
            confidence=0.50,
            suggested_actions=["Ver Relatório", "Saldo Atual", "Dicas de Economia"]
        )

    def _try_llm_completion(self, message: str, history: list[dict] = None) -> Optional[str]:
        """Tenta consultar modelos LLM na OpenRouter com failover ordenado em caso de rate-limit (429)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        # Lista ordenada de modelos candidatos (evita duplicatas)
        candidates = [self.model, "inclusionai/ling-3.0-flash-fin:free", "minimax/minimax-m3:free", "liquid/lfm-2.5-2.6b:free"]
        seen = set()
        model_list = [m for m in candidates if m and not (m in seen or seen.add(m))]

        for model_name in model_list:
            payload = {
                "model": model_name,
                "messages": messages
            }
            try:
                response = requests.post(
                    url=f"{self.base_url}/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    choice = data['choices'][0]['message']
                    content = choice.get('content', '')
                    if not content and 'reasoning_details' in choice:
                        content = choice['reasoning_details'].get('text', '')
                    if content and content.strip():
                        return content.strip()
                else:
                    logger.warning(f"Modelo {model_name} retornou status {response.status_code}. Tentando próximo candidato...")
            except Exception as e:
                logger.warning(f"Erro ao chamar modelo {model_name}: {e}. Tentando próximo candidato...")

        return None

    def _get_local_concept_explanation(self, msg_lower: str) -> Optional[str]:
        """Base de conhecimento determinística para conceitos essenciais quando o LLM estiver indisponível."""
        if "selic" in msg_lower:
            return (
                "### 🏦 O que é a Taxa Selic?\n"
                "A **Taxa Selic** é a taxa básica de juros da economia brasileira, definida a cada 45 dias pelo Comitê de Política Monetária (Copom) do Banco Central.\n\n"
                "- **Como funciona:** É a taxa média dos empréstimos diários entre bancos lastreados em títulos públicos federais.\n"
                "- **Impacto no crédito:** Quando a Selic sobe, empréstimos, cartões de crédito e financiamentos ficam mais caros, desacelerando o consumo para conter a inflação. Quando ela cai, o crédito fica mais barato.\n"
                "- **Impacto nos investimentos:** Investimentos de renda fixa pós-fixados (como o **Tesouro Selic** e **CDBs de liquidez diária a 100% do CDI**) aumentam sua rentabilidade quando a Selic está elevada."
            )

        if "cdi" in msg_lower:
            return (
                "### 📈 O que é o CDI?\n"
                "O **CDI** (Certificado de Depósito Interbancário) é o título que os bancos emitem para emprestar dinheiro uns aos outros no prazo de 1 dia útil.\n\n"
                "- **Relação com a Selic:** A taxa DI (CDI) acompanha a meta da Selic muito de perto, situando-se geralmente cerca de 0,10 ponto percentual abaixo dela.\n"
                "- **Referência de Renda Fixa:** É a régua mais comum do mercado. Quando uma conta remunerada ou CDB promete '100% do CDI', significa que você recebe exatamente a taxa média de juros interbancários do país."
            )

        if "reserva de emergência" in msg_lower or "reserva de emergencia" in msg_lower:
            return (
                "### 🛡️ O que é a Reserva de Emergência?\n"
                "A **Reserva de Emergência** é o colchão de segurança financeiro destinado exclusivamente a imprevistos (problemas de saúde, desemprego repentino, reparos urgentes na casa ou veículo).\n\n"
                "- **Quanto guardar:** O equivalente a **3 a 6 meses** de todos os seus custos de vida fixos essenciais.\n"
                "- **Onde aplicar:** Deve ficar em aplicações de **altíssima segurança e liquidez diária** (dinheiro na mão no mesmo dia), como Tesouro Selic ou CDBs com liquidez diária garantidos pelo FGC."
            )

        if "inflação" in msg_lower or "inflacao" in msg_lower or "ipca" in msg_lower:
            return (
                "### 📉 O que é Inflação e IPCA?\n"
                "A **Inflação** é a alta contínua e generalizada dos preços de produtos e serviços, que reduz o poder de compra do seu dinheiro com o passar do tempo.\n\n"
                "- **IPCA:** É o Índice Nacional de Preços ao Consumidor Amplo, o indicador oficial de inflação no Brasil medido pelo IBGE.\n"
                "- **Como se defender:** Investir o dinheiro em ativos que paguem uma taxa superior à inflação (ganho real), como títulos do Tesouro IPCA+."
            )

        if "juros compostos" in msg_lower:
            return (
                "### ⏳ O que são Juros Compostos?\n"
                "São os juros calculados sobre o capital inicial acrescido dos juros já acumulados nos períodos anteriores ('juros sobre juros').\n\n"
                "- **Efeito exponencial:** No início o crescimento parece modesto, mas com o passar dos anos o efeito gera uma aceleração poderosa na multiplicação do patrimônio."
            )

        return None
