from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class AgentContext:
    """Contexto compartilhado fornecido aos agentes especializados."""
    message: str
    history: list[dict[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResult:
    """Resultado estruturado padronizado produzido por qualquer agente especializado."""
    reply: str
    agent_name: str
    confidence: float = 1.0
    pending_transaction: Optional[dict] = None
    report_data: Optional[dict] = None
    action_taken: Optional[str] = None
    suggested_actions: list[str] = field(default_factory=list)

class BaseAgent(ABC):
    """Contrato base para qualquer agente financeiro especializado."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def can_handle(self, context: AgentContext) -> float:
        """
        Retorna uma pontuação de 0.0 a 1.0 indicando a afinidade/confiança do agente
        em responder com excelência à mensagem do contexto.
        """
        pass

    @abstractmethod
    def process(self, context: AgentContext) -> AgentResult:
        """
        Executa a tarefa especializada utilizando ferramentas e lógica de domínio,
        retornando o resultado padronizado.
        """
        pass
