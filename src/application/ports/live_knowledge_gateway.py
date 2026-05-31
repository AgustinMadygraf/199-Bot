"""
Path: src/application/ports/live_knowledge_gateway.py
"""

from typing import Protocol

class LiveKnowledgeGateway(Protocol):
    async def get_live_knowledge(self, consulta: str) -> str:
        ...
