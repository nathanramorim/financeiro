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
                timeout=30
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
        
        if any(term in msg_lower for term in ["dividir por 2", "divida por 2", "dividida por 2", "/ 2", "dividir por"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Divididas por 2:"]
            for exp in fixed_expenses:
                valor_original = float(exp['Valor'])
                valor_div = MathTool.divide(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_div:.2f}**")
            return "\n".join(res)

        if any(term in msg_lower for term in ["multiplicar por 2", "multiplique por 2", "multiplicado por 2", "* 2"]):
            fixed_expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 🧮 Despesas Fixas Multiplicadas por 2:"]
            for exp in fixed_expenses:
                valor_original = float(exp['Valor'])
                valor_mult = MathTool.multiply(valor_original, 2)
                res.append(f"- **{exp['Descrição']}**: R$ {valor_original:.2f} ➔ **R$ {valor_mult:.2f}**")
            return "\n".join(res)

        if "saldo" in msg_lower or "balanço" in msg_lower:
            bal = self.income_tool.get_balance()
            return (
                f"### 💰 Resumo do Saldo Atual\n"
                f"- **Total de Receitas:** R$ {bal['total_receitas']:.2f}\n"
                f"- **Total de Despesas:** R$ {bal['total_despesas']:.2f}\n"
                f"- **Saldo Líquido:** **R$ {bal['saldo_liquido']:.2f}**"
            )

        # Adição de despesas (ex: "adicionei despesa Aluguel 1500", "cadastrar despesa Mercado R$ 200")
        if any(term in msg_lower for term in ["adicion", "cadastrar", "incluir", "nova despesa", "novo gasto"]):
            import re
            numbers = re.findall(r"r\$\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)", msg_lower)
            valor = 0.0
            for n in numbers:
                val_str = n[0] or n[1]
                if val_str:
                    try:
                        valor = float(val_str.replace(',', '.'))
                        if valor > 0:
                            break
                    except ValueError:
                        pass
            
            # Tentar extrair descrição simples excluindo palavras de comando
            tokens = [t for t in msg.split() if t.lower() not in ["adicionar", "adicionei", "cadastrar", "incluir", "despesa", "gasto", "r$", "de", "com", "uma", "um"]]
            descricao = " ".join([t for t in tokens if not re.match(r"^\d+(?:[.,]\d+)?$", t)]) or "Despesa Genérica"

            if valor > 0:
                item = self.expense_tool.add_expense(descricao=descricao, valor=valor, tipo="fixa")
                return f"✅ **Despesa cadastrada com sucesso!**\n- **Descrição:** {item['Descrição']}\n- **Valor:** R$ {item['Valor']:.2f}\n- **Categoria:** {item['Categoria']}\n- **Tipo:** {item['Tipo']}"
            else:
                return "⚠️ Por favor, informe o valor da despesa para realizar o cadastro (ex: *Adicionei despesa Mercado R$ 150*)."

        if "despesa" in msg_lower or "gastos" in msg_lower:
            expenses = self.expense_tool.list_fixed_expenses()
            res = ["### 📋 Despesas Fixas Cadastradas:"]
            for exp in expenses:
                res.append(f"- **{exp['Descrição']}** ({exp['Categoria']}): R$ {float(exp['Valor']):.2f}")
            return "\n".join(res)

        return "Recebi sua mensagem financeira e processei as informações com sucesso."
