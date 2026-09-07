from services.langgraph_service import ChatboxdAgent
from services.llm_service import build_llm


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, ChatboxdAgent] = {}

    def _key(self, session_id: str, provider: str, model: str, language: str) -> str:
        return f"{session_id}|{provider}|{model}|{language}"

    def get_or_create(
        self, session_id: str, provider: str, model: str, language: str
    ) -> ChatboxdAgent:
        key = self._key(session_id, provider, model, language)
        agent = self._agents.get(key)
        if agent is None:
            agent = ChatboxdAgent(
                llm=build_llm(provider, model),
                language=language,
            )
            self._agents[key] = agent
        return agent

    def reset(self, session_id: str) -> None:
        prefix = f"{session_id}|"
        for key in [k for k in self._agents if k.startswith(prefix)]:
            del self._agents[key]


registry = AgentRegistry()
