# Feature e4b1-01 — Fundação e Contratos Multiagente

## Contexto e Objetivo
Estabelecer a espinha dorsal técnica da arquitetura multiagente para o backend FastAPI. Definir os contratos abstratos, modelos de dados de contexto e resposta padronizados e o catálogo dinâmico (`AgentRegistry`) para permitir que agentes especializados sejam registrados e descobertos de forma desacoplada (Plug-and-play), em estrita observância à Clean Architecture (`.agents/rules/arquitetura.md`).

## Escopo e Especificações
1. **Modelos de Dados do Domínio de Agentes (`src/agent/base.py`):**
   - `AgentContext`:
     - `message: str`: texto de entrada da mensagem do usuário.
     - `history: list[dict[str, str]]`: histórico conversacional.
     - `metadata: dict[str, Any]`: dados de contexto adicionais (ex: user_id, timestamps, intenções pré-classificadas).
   - `AgentResult`:
     - `reply: str`: resposta final gerada para o usuário.
     - `agent_name: str`: identificador do agente executor.
     - `confidence: float`: nível de confiança da execução (0.0 a 1.0).
     - `pending_transaction: Optional[dict]`: dados de transação a ser confirmada.
     - `report_data: Optional[dict]`: dados analíticos/estruturados para renderização de gráficos.
     - `action_taken: Optional[str]`: ação executada ou sugerida.
     - `suggested_actions: list[str]`: atalhos/chips de respostas rápidas para a UI.
2. **Interface Abstrata do Agente (`BaseAgent` em `src/agent/base.py`):**
   - Propriedades obrigatórias: `name: str`, `description: str`.
   - Método `can_handle(self, context: AgentContext) -> float`: avalia a intenção e retorna pontuação de afinidade (0.0 = incapaz, 1.0 = especialista exato).
   - Método `process(self, context: AgentContext) -> AgentResult`: executa a tarefa especializada.
3. **Catálogo de Agentes (`AgentRegistry` em `src/agent/registry.py`):**
   - Métodos:
     - `register(agent: BaseAgent) -> None`: adiciona o agente ao registro.
     - `unregister(name: str) -> bool`: remove agente do catálogo.
     - `get(name: str) -> Optional[BaseAgent]`: busca agente por nome.
     - `get_all() -> list[BaseAgent]`: lista todos os agentes registrados.
     - `find_best_agent(context: AgentContext) -> tuple[Optional[BaseAgent], float]`: consulta o método `can_handle` de todos os agentes e seleciona o mais qualificado.
4. **Testes Automatizados (`tests/test_agent_core.py`):**
   - Teste de instanciação de `BaseAgent` derivado.
   - Teste de registro, desregistro e busca no `AgentRegistry`.
   - Teste de desempate e seleção de melhor agente via `find_best_agent`.

## Critérios de Aceite
- [x] `BaseAgent`, `AgentContext` e `AgentResult` implementados com tipagem estrita via dataclasses ou Pydantic.
- [x] `AgentRegistry` implementa registro dinâmico e seleção por afinidade sem dependências de frameworks de apresentação.
- [x] Suíte `tests/test_agent_core.py` implementada e passando com 100% de cobertura nos contratos base via `uv run pytest`.
