import re
from typing import Optional
from backend.agent.base import BaseAgent, AgentContext, AgentResult
from backend.agent.prompts import TRANSACTION_AGENT_PROMPT
from backend.tools.expenses import ExpenseTool
from backend.tools.income import IncomeTool
from backend.tools.category import CategoryTool
from backend.tools.math_tool import MathTool

class TransactionAgent(BaseAgent):
    """Especialista em detecção, estruturação, confirmação e execução de receitas e despesas."""

    def __init__(self, expense_tool: Optional[ExpenseTool] = None, income_tool: Optional[IncomeTool] = None):
        super().__init__(
            name="transaction_agent",
            description="Especialista em detecção, parsing, validação e execução de receitas e despesas financeiras."
        )
        self.system_prompt = TRANSACTION_AGENT_PROMPT
        self.expense_tool = expense_tool or ExpenseTool()
        self.income_tool = income_tool or IncomeTool()

    def can_handle(self, context: AgentContext) -> float:
        msg_lower = context.message.lower()

        # Gatilhos fortes de mutação ou transação
        is_tx_action = any(term in msg_lower for term in [
            "add despesa", "add receita", "adicionar despesa", "adicionar receita",
            "adicionei despesa", "adicionei receita", "cadastrar despesa", "cadastrar receita",
            "incluir despesa", "incluir receita", "nova despesa", "novo gasto",
            "atualizar despesa", "atualizar receita", "editar despesa", "editar receita"
        ])
        if is_tx_action:
            return 0.98

        has_money_action = any(term in msg_lower for term in ["gastei", "comprei", "paguei", "ganhei", "recebi"]) and re.search(r"\d+", msg_lower)
        if has_money_action:
            return 0.90

        if any(term in msg_lower for term in ["despesa", "receita"]) and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "nova", "novo"]):
            return 0.85

        return 0.05

    def detect_mutation_intent(self, message: str) -> Optional[dict]:
        msg_lower = message.lower()

        # Receita
        is_receita_cmd = any(term in msg_lower for term in ["receita", "ganhei", "provento"]) and any(
            term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "atualizar", "editar", "nova", "novo"]
        )
        if is_receita_cmd or "add receita" in msg_lower or "atualizar receita" in msg_lower:
            numbers = re.findall(r"r\$\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)", msg_lower)
            valor = 0.0
            for n in numbers:
                val_str = n[0] or n[1]
                if val_str:
                    v = MathTool.parse_float(val_str)
                    if v > 0:
                        valor = v
                        break
            tokens = [
                t for t in message.split()
                if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "atualizar", "editar", "receita", "ganho", "provento", "r$", "de", "com", "uma", "um"]
            ]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Receita Genérica"
            if valor > 0:
                is_update = "atualizar" in msg_lower or "editar" in msg_lower
                return {
                    "action": "update_income" if is_update else "add_income",
                    "action_label": "Atualizar Receita" if is_update else "Adicionar Receita",
                    "descricao": descricao,
                    "valor": valor,
                    "tipo": "receita"
                }

        # Despesa
        is_despesa_cmd = any(term in msg_lower for term in [
            "add despesa", "adicionar despesa", "adicionei despesa", "cadastrar despesa",
            "incluir despesa", "nova despesa", "novo gasto", "atualizar despesa", "editar despesa"
        ]) or ("despesa" in msg_lower and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "atualizar", "editar", "nova", "novo"])) or any(term in msg_lower for term in ["gastei", "comprei", "paguei"])
        if is_despesa_cmd:
            numbers = re.findall(r"r\$\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)", msg_lower)
            valor = 0.0
            for n in numbers:
                val_str = n[0] or n[1]
                if val_str:
                    v = MathTool.parse_float(val_str)
                    if v > 0:
                        valor = v
                        break
            tokens = [
                t for t in message.split()
                if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "atualizar", "editar", "despesa", "gasto", "gastei", "comprei", "paguei", "r$", "de", "com", "uma", "um"]
            ]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Despesa Genérica"
            categoria = CategoryTool.categorize(descricao)
            if valor > 0:
                is_update = "atualizar" in msg_lower or "editar" in msg_lower
                return {
                    "action": "update_expense" if is_update else "add_expense",
                    "action_label": "Atualizar Despesa" if is_update else "Adicionar Despesa",
                    "descricao": descricao,
                    "valor": valor,
                    "categoria": categoria,
                    "tipo": "fixa"
                }

        return None

    def execute_transaction(self, tx: dict) -> str:
        action = tx.get("action")
        descricao = tx.get("descricao", "Registro")
        valor = MathTool.parse_float(tx.get("valor", 0.0))
        tipo = tx.get("tipo", "fixa")
        categoria = tx.get("categoria")

        if action in ["add_expense", "update_expense"]:
            item = self.expense_tool.add_expense(descricao=descricao, valor=valor, tipo=tipo, categoria=categoria)
            label = "atualizada" if "update" in action else "cadastrada"
            return f"✅ **Despesa {label} e confirmada com sucesso!**\n- **Descrição:** {item['Descrição']}\n- **Valor:** R$ {MathTool.parse_float(item['Valor']):.2f}\n- **Categoria:** {item['Categoria']}\n- **Tipo:** {item['Tipo']}"

        elif action in ["add_income", "update_income"]:
            item = self.income_tool.add_income(descricao=descricao, valor=valor)
            label = "atualizada" if "update" in action else "cadastrada"
            return f"✅ **Receita {label} e confirmada com sucesso!**\n- **Descrição:** {item['Descrição']}\n- **Valor:** R$ {MathTool.parse_float(item['Valor']):.2f}"

        return "⚠️ Ação desconhecida ou não processada."

    def process(self, context: AgentContext) -> AgentResult:
        tx = self.detect_mutation_intent(context.message)
        if tx:
            desc = tx.get("descricao", "Registro")
            val = tx.get("valor", 0.0)
            label = tx.get("action_label", "Adicionar")
            reply = f"📋 Deseja confirmar a seguinte ação?\n\n**Operação:** {label}\n**Descrição:** {desc}\n**Valor:** R$ {val:.2f}"
            return AgentResult(
                reply=reply,
                agent_name=self.name,
                confidence=0.98,
                pending_transaction=tx,
                suggested_actions=["Confirmar", "Cancelar"]
            )

        # Se tentou adicionar mas faltou o valor
        msg_lower = context.message.lower()
        if "receita" in msg_lower:
            reply = "⚠️ Por favor, informe o valor da receita para realizar o cadastro (ex: *Add receita Freelance R$ 500*)."
        else:
            reply = "⚠️ Por favor, informe o valor da despesa para realizar o cadastro (ex: *Add despesa Mercado R$ 150*)."

        return AgentResult(
            reply=reply,
            agent_name=self.name,
            confidence=0.70
        )
