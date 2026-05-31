"""
Path: src/application/ports/tutor_ports.py
"""

from typing import Protocol, Iterable, List
from src.domain.entities.chat_message import ChatMessage

class LLMClient(Protocol):
    async def generar_respuesta(self, messages: Iterable[ChatMessage]) -> str:
        ...

class KnowledgeRepository(Protocol):
    def buscar_reglamento(self, consulta: str) -> str:
        ...

    async def obtener_datos_vivos(self, consulta: str) -> str:
        ...
    @property
    def static_knowledge(self) -> str:
        ...

class HistoryRepository(Protocol):
    def cargar(self, user_id: int) -> List[ChatMessage]:
        ...
    def guardar(self, user_id: int, historial: List[ChatMessage]) -> None:
        ...
    def borrar(self, user_id: int) -> None:
        ...
