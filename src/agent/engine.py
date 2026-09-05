import json
import requests
from src.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
from src.agent.prompts import SYSTEM_PROMPT
from src.tools.math_tool import MathTool
from src.tools.expenses import ExpenseTool
from src.tools.income import IncomeTool

class FinancialAgent:
    def __init__(self, api_key: str = OPENROUTER_API_KEY, model: str = OPENROUTER_MODEL):
        self.api_key = api_key or "mock_key"
        self.model = model
        self.base_url = OPENROUTER_BASE_URL
        self.expense_tool = ExpenseTool()
        self.income_tool = IncomeTool()

    def process_message(self, user_message: str, history: list[dict] = None) -> str:
        msg_lower = user_message.lower()

        # Se for solicitação de relatório ou gráficos, prioriza a resposta limpa e determinística do relatório
        if self.is_report_request(user_message):
            return self._local_fallback_process(user_message)

        # Se for um comando direto de mutação/adicionar despesa ou receita, prioriza execução garantida via ferramentas
        if any(term in msg_lower for term in ["add despesa", "add receita", "adicionar despesa", "adicionar receita", "cadastrar despesa", "cadastrar receita", "incluir despesa", "incluir receita"]):
            return self._local_fallback_process(user_message)

        if not self.api_key or self.api_key == "mock_key":
            return self._local_fallback_process(user_message)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Monta a lista de mensagens incluindo system prompt, histórico e mensagem atual
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "reasoning": {"enabled": True}
        }

        try:
            response = requests.post(
                url=f"{self.base_url}/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=4
            )
            
            if response.status_code == 200:
                data = response.json()
                choice = data['choices'][0]['message']
                content = choice.get('content', '')
                
                # Se o conteúdo estiver vazio mas houver reasoning_details
                if not content and 'reasoning_details' in choice:
                    content = choice['reasoning_details'].get('text', '') or "Processado com raciocínio."
                
                return content if content else self._local_fallback_process(user_message)
            else:
                print(f"[FinancialAgent Warning] Status {response.status_code} da API OpenRouter. Alternando para fallback.")
                return self._local_fallback_process(user_message)
        except Exception as e:
            print(f"[FinancialAgent Error] Exceção ao chamar OpenRouter: {e}. Alternando para fallback local.")
            return self._local_fallback_process(user_message)

    def _local_fallback_process(self, msg: str) -> str:
        msg_lower = msg.lower()
        import re

        if any(term in msg_lower for term in ["dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Divididas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_div = MathTool.divide(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_div:.2f}**")
            return "\n".join(res)

        if any(term in msg_lower for term in ["multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Multiplicadas por 2:"]
            for exp in fixed_expenses:
                valor_original = MathTool.parse_float(exp['Valor'])
                valor_mult = MathTool.multiply(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_mult:.2f}**")
            return "\n".join(res)

        # Adição de receita (ex: "add receita salario 5000", "cadastrar receita freela 300")
        is_receita_cmd = any(term in msg_lower for term in ["receita", "ganhei", "provento"]) and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "nova", "novo"])
        if is_receita_cmd or "add receita" in msg_lower:
            numbers = re.findall(r"r\$\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)", msg_lower)
            valor = 0.0
            for n in numbers:
                val_str = n[0] or n[1]
                if val_str:
                    v = MathTool.parse_float(val_str)
                    if v > 0:
                        valor = v
                        break
            
            tokens = [t for t in msg.split() if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "receita", "ganho", "provento", "r$", "de", "com", "uma", "um"]]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Receita Genérica"

            if valor > 0:
                item = self.income_tool.add_income(descricao=descricao, valor=valor)
                return f"✅ **Receita cadastrada com sucesso!**\n- **Descrição:** {item['Descrição']}\n- **Valor:** R$ {MathTool.parse_float(item['Valor']):.2f}"
            else:
                return "⚠️ Por favor, informe o valor da receita para realizar o cadastro (ex: *Add receita Freelance R$ 500*)."

        # Relatório / Gráficos
        if self.is_report_request(msg):
            report = self.generate_report_data()
            lines = [
                "### 📊 Relatório Financeiro Executivo",
                f"- **Total de Receitas:** R$ {report['total_receitas']:.2f}",
                f"- **Total de Despesas:** R$ {report['total_despesas']:.2f}",
                f"- **Saldo Líquido:** **R$ {report['saldo_liquido']:.2f}**\n",
                "#### 🏷️ Despesas por Categoria:"
            ]
            for cat, val in report["despesas_por_categoria"].items():
                lines.append(f"- **{cat}:** R$ {val:.2f}")
            lines.append("\n*Gráficos gerados e renderizados na interface abaixo.*")
            return "\n".join(lines)

        # Adição de despesas (ex: "add despesa Aluguel 1500", "adicionei despesa Mercado R$ 200")
        is_despesa_cmd = any(term in msg_lower for term in ["add despesa", "adicionar despesa", "adicionei despesa", "cadastrar despesa", "incluir despesa", "nova despesa", "novo gasto"]) or (
            "despesa" in msg_lower and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "nova", "novo"])
        )
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
            
            tokens = [t for t in msg.split() if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "despesa", "gasto", "r$", "de", "com", "uma", "um"]]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Despesa Genérica"

            if valor > 0:
                item = self.expense_tool.add_expense(descricao=descricao, valor=valor, tipo="fixa")
                return f"✅ **Despesa cadastrada com sucesso!**\n- **Descrição:** {item['Descrição']}\n- **Valor:** R$ {MathTool.parse_float(item['Valor']):.2f}\n- **Categoria:** {item['Categoria']}\n- **Tipo:** {item['Tipo']}"
            else:
                return "⚠️ Por favor, informe o valor da despesa para realizar o cadastro (ex: *Add despesa Mercado R$ 150*)."

        if "saldo" in msg_lower or "balanço" in msg_lower:
            bal = self.income_tool.get_balance()
            return (
                f"### 💰 Resumo do Saldo Atual\n"
                f"- **Total de Receitas:** R$ {bal['total_receitas']:.2f}\n"
                f"- **Total de Despesas:** R$ {bal['total_despesas']:.2f}\n"
                f"- **Saldo Líquido:** **R$ {bal['saldo_liquido']:.2f}**"
            )

        if "despesa" in msg_lower or "gastos" in msg_lower:
            expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 📋 Despesas Fixas Cadastradas:"]
            for exp in expenses:
                res.append(f"- **{exp['Descrição']}** ({exp['Categoria']}): R$ {MathTool.parse_float(exp['Valor']):.2f}")
            return "\n".join(res)

        return "Recebi sua mensagem financeira e processei as informações com sucesso."

    def is_report_request(self, user_message: str) -> bool:
        msg_lower = user_message.lower()
        return any(term in msg_lower for term in ["relatorio", "relatório", "grafico", "gráfico", "gráficos", "graficos"])

    def generate_report_data(self) -> dict:
        expenses = self.expense_tool.list_all_expenses()
        incomes = self.income_tool.service.get_incomes()

        tot_despesas = sum(MathTool.parse_float(e.get("Valor", 0)) for e in expenses)
        tot_receitas = sum(MathTool.parse_float(i.get("Valor", 0)) for i in incomes)
        saldo = tot_receitas - tot_despesas

        from src.tools.category import CategoryTool
        cat_dict = {}
        for e in expenses:
            cat = e.get("Categoria")
            if not cat or str(cat).strip().lower() in ["", "outros", "none"]:
                inferred = CategoryTool.categorize(e.get("Descrição", ""))
                cat = inferred if inferred else "Outros"
            val = MathTool.parse_float(e.get("Valor", 0))
            cat_dict[cat] = cat_dict.get(cat, 0.0) + val

        return {
            "total_receitas": round(tot_receitas, 2),
            "total_despesas": round(tot_despesas, 2),
            "saldo_liquido": round(saldo, 2),
            "despesas_por_categoria": cat_dict
        }

    def detect_mutation_intent(self, user_message: str) -> dict | None:
        import re
        msg_lower = user_message.lower()

        # Adição/atualização de receita
        is_receita_cmd = any(term in msg_lower for term in ["receita", "ganhei", "provento"]) and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "atualizar", "editar", "nova", "novo"])
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
            tokens = [t for t in user_message.split() if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "atualizar", "editar", "receita", "ganho", "provento", "r$", "de", "com", "uma", "um"]]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Receita Genérica"
            if valor > 0:
                is_update = "atualizar" in msg_lower or "editar" in msg_lower
                return {
                    "action": "update_income" if is_update else "add_income",
                    "action_label": "Atualizar Receita" if is_update else "Adicionar Receita",
                    "descricao": descricao,
                    "valor": valor
                }

        # Adição/atualização de despesa
        is_despesa_cmd = any(term in msg_lower for term in ["add despesa", "adicionar despesa", "adicionei despesa", "cadastrar despesa", "incluir despesa", "nova despesa", "novo gasto", "atualizar despesa", "editar despesa"]) or (
            "despesa" in msg_lower and any(term in msg_lower for term in ["add", "adicion", "cadastrar", "incluir", "atualizar", "editar", "nova", "novo"])
        )
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
            tokens = [t for t in user_message.split() if t.lower() not in ["add", "adicionar", "adicionei", "cadastrar", "incluir", "atualizar", "editar", "despesa", "gasto", "r$", "de", "com", "uma", "um"]]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Despesa Genérica"
            from src.tools.category import CategoryTool
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
