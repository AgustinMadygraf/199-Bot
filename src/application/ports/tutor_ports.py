"""
Path: src/application/port/tutor_ports.py
"""

from typing import Protocol, List, Dict

class LLMClient(Protocol):
    async def generar_respuesta(self, messages: List[Dict[str, str]]) -> str:
        ...

class KnowledgeRepository(Protocol):
    def buscar_reglamento(self, consulta: str) -> str:
        ...
    def obtener_datos_vivos(self, consulta: str) -> str:
        ...
    @property
    def static_knowledge(self) -> str:
        ...

class HistoryRepository(Protocol):
    def cargar(self, user_id: int) -> List[Dict[str, str]]:
        ...
    def guardar(self, user_id: int, historial: List[Dict[str, str]]) -> None:
        ...
