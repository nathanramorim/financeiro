# Guia de Desenvolvimento de Agentes Especializados (Multiagente)

Este guia orienta engenheiros e analistas na criação e registro de novos agentes especializados na malha multiagente do **Financeiro**.

---

## 1. Princípios de Design e Clean Architecture

A arquitetura do assistente financeiro adota o padrão **Supervisor / Workers (Router + Especialistas)**:
1. **Desacoplamento Total:** Cada especialista encapsula regras de seu próprio subdomínio financeiro (ex: transações, metas, consultoria, relatórios, investimentos).
2. **Princípio Aberto/Fechado (SOLID):** Para adicionar uma nova capacidade à API, **nenhuma rota** ou arquivo do Presentation Layer precisa ser modificado. Basta criar o novo agente e registrá-lo no `AgentRegistry`.
3. **Determinismo Aritmético:** Nenhuma conta ou agregação financeira deve ser delegada a texto livre de LLMs. Utilize sempre o `MathTool` ou rotinas analíticas do Python.

---

## 2. Passo a Passo para Criar um Novo Agente

### Passo 2.1: Estender `BaseAgent`
Crie um arquivo em `src/agent/specialists/<nome_do_agente>.py`:

```python
from src.agent.base import BaseAgent, AgentContext, AgentResult

class MeuNovoEspecialista(BaseAgent):
    def __init__(self):
        super().__init__(
            name="meu_novo_especialista",
            description="Descrição clara do subdomínio e das capacidades do agente."
        )

    def can_handle(self, context: AgentContext) -> float:
        """
        Avalia o texto da mensagem do usuário e retorna um score de 0.0 a 1.0:
        - 0.90 a 1.00: Intenção exata e domínio direto deste agente.
        - 0.50 a 0.89: Intenção parcialmente relacionada.
        - 0.00 a 0.49: Fora do escopo deste especialista.
        """
        msg_lower = context.message.lower()
        if "palavra_chave" in msg_lower:
            return 0.95
        return 0.10

    def process(self, context: AgentContext) -> AgentResult:
        """
        Executa a tarefa utilizando ferramentas de infraestrutura (Tools/Services)
        e retorna um AgentResult estruturado.
        """
        resposta_formatada = "### Resposta do Novo Especialista\n..."
        return AgentResult(
            reply=resposta_formatada,
            agent_name=self.name,
            confidence=0.95,
            suggested_actions=["Ação 1", "Ação 2"]
        )
```

---

### Passo 2.2: Registrar o Novo Agente no Roteador
No ponto de composição da aplicação (`src/agent/router.py`) ou dinamicamente na inicialização do serviço:

```python
from src.agent.router import AgentRouter
from src.agent.specialists.meu_novo_especialista import MeuNovoEspecialista

router = AgentRouter()
router.registry.register(MeuNovoEspecialista())
```

Pronto! A partir deste momento, qualquer requisição enviada ao endpoint `POST /api/chat` cuja mensagem ative a afinidade do novo agente será automaticamente direcionada a ele pelo `AgentRouter`.

---

### Passo 2.3: Criar os Testes Unitários
Adicione os testes correspondentes em `tests/test_specialist_agents.py`:
- Teste unitário de `can_handle`: valida se as palavras-chave ativam o score esperado.
- Teste unitário de `process`: valida a resposta, campos estruturados e ausência de regressões.

Execute os testes via:
```bash
uv run pytest tests/test_specialist_agents.py
```
