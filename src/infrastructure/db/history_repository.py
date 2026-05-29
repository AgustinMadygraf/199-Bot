"""
Path: src/infrastructure/db/history_repository.py
"""

from typing import List
from groq.types.chat import ChatCompletionMessageParam
from src.infrastructure.db import cargar_historial, guardar_historial

class DBHistoryRepository:
    def cargar(self, user_id: int) -> List[ChatCompletionMessageParam]:
        return cargar_historial(user_id)
        
    def guardar(self, user_id: int, historial: List[ChatCompletionMessageParam]) -> None:
        guardar_historial(user_id, historial)
