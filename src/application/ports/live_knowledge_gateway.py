from typing import Protocol

class LiveKnowledgeGateway(Protocol):
    async def get_live_knowledge(self, consulta: str) -> str:
        ...
