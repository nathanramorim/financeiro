from typing import Optional
from src.agent.base import BaseAgent, AgentContext

class AgentRegistry:
    """Catálogo dinâmico para registro e descoberta de agentes especializados."""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Registra uma instância de agente no catálogo."""
        self._agents[agent.name] = agent

    def unregister(self, name: str) -> bool:
        """Remove um agente pelo seu nome identificador."""
        if name in self._agents:
            del self._agents[name]
            return True
        return False

    def get(self, name: str) -> Optional[BaseAgent]:
        """Obtém um agente pelo nome exato."""
        return self._agents.get(name)

    def get_all(self) -> list[BaseAgent]:
        """Retorna a lista de todos os agentes ativos cadastrados."""
        return list(self._agents.values())

    def find_best_agent(self, context: AgentContext) -> tuple[Optional[BaseAgent], float]:
        """
        Consulta todos os agentes registrados e retorna o agente com maior pontuação
        de afinidade (`can_handle`), junto com sua pontuação.
        """
        best_agent: Optional[BaseAgent] = None
        highest_score = -1.0

        for agent in self._agents.values():
            try:
                score = agent.can_handle(context)
            except Exception as e:
                print(f"[AgentRegistry Warning] Erro ao avaliar afinidade do agente {agent.name}: {e}")
                score = 0.0

            if score > highest_score:
                highest_score = score
                best_agent = agent

        return best_agent, max(0.0, highest_score)
