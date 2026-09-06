import pytest
from backend.agent.base import BaseAgent, AgentContext, AgentResult
from backend.agent.registry import AgentRegistry

class DummyHighAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="dummy_high", description="Dummy agent with high confidence")

    def can_handle(self, context: AgentContext) -> float:
        if "investimento" in context.message.lower():
            return 0.95
        return 0.1

    def process(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            reply="Resposta de investimentos.",
            agent_name=self.name,
            confidence=0.95
        )

class DummyLowAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="dummy_low", description="Dummy agent with low confidence")

    def can_handle(self, context: AgentContext) -> float:
        return 0.3

    def process(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            reply="Resposta genérica.",
            agent_name=self.name,
            confidence=0.3
        )

class FaultyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="faulty", description="Faulty agent that raises an exception")

    def can_handle(self, context: AgentContext) -> float:
        raise RuntimeError("Falha de teste")

    def process(self, context: AgentContext) -> AgentResult:
        raise RuntimeError("Erro ao processar")

def test_agent_context_and_result_defaults():
    ctx = AgentContext(message="Olá finanças")
    assert ctx.message == "Olá finanças"
    assert ctx.history == []
    assert ctx.metadata == {}

    res = AgentResult(reply="Tudo certo", agent_name="test_agent")
    assert res.reply == "Tudo certo"
    assert res.agent_name == "test_agent"
    assert res.confidence == 1.0
    assert res.pending_transaction is None
    assert res.report_data is None
    assert res.action_taken is None
    assert res.suggested_actions == []

def test_base_agent_is_abstract():
    with pytest.raises(TypeError):
        BaseAgent(name="abs", description="abstract")

def test_registry_register_and_get():
    registry = AgentRegistry()
    high_agent = DummyHighAgent()
    low_agent = DummyLowAgent()

    registry.register(high_agent)
    registry.register(low_agent)

    assert registry.get("dummy_high") is high_agent
    assert registry.get("dummy_low") is low_agent
    assert registry.get("inexistente") is None
    assert len(registry.get_all()) == 2

    # Unregister
    assert registry.unregister("dummy_low") is True
    assert registry.unregister("dummy_low") is False
    assert registry.get("dummy_low") is None
    assert len(registry.get_all()) == 1

def test_registry_find_best_agent():
    registry = AgentRegistry()
    high_agent = DummyHighAgent()
    low_agent = DummyLowAgent()
    faulty_agent = FaultyAgent()

    registry.register(high_agent)
    registry.register(low_agent)
    registry.register(faulty_agent)

    # 1. Mensagem com "investimento": DummyHighAgent deve vencer com 0.95
    ctx1 = AgentContext(message="Dúvida sobre investimento em CDB")
    best1, score1 = registry.find_best_agent(ctx1)
    assert best1 is high_agent
    assert score1 == 0.95

    # 2. Mensagem genérica: DummyLowAgent deve vencer com 0.3 (DummyHighAgent dá 0.1)
    ctx2 = AgentContext(message="Como você está?")
    best2, score2 = registry.find_best_agent(ctx2)
    assert best2 is low_agent
    assert score2 == 0.3
