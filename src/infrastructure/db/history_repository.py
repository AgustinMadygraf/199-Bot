"""
Path: src/application/ports/tutor_ports.py
"""

from typing import List, Dict, cast
from src.infrastructure.db.sqlite_handler import cargar_historial, guardar_historial, borrar_historial # type: ignore
from src.domain.entities.chat_message import ChatMessage
from src.application.ports.tutor_ports import HistoryRepository

class DBHistoryRepository(HistoryRepository):
    def cargar(self, user_id: int) -> List[ChatMessage]:
        raw_historial = cast(List[Dict[str, str]], cargar_historial(user_id))
        return [ChatMessage(role=msg["role"], content=msg["content"]) for msg in raw_historial]
        
    def guardar(self, user_id: int, historial: List[ChatMessage]) -> None:
        raw_historial: List[Dict[str, str]] = [
            {"role": msg.role, "content": msg.content} for msg in historial
        ]
        guardar_historial(user_id, raw_historial)
        
    def borrar(self, user_id: int) -> None:
        borrar_historial(user_id)
