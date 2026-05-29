"""
Path: src/infrastructure/db/history_repository.py
"""

from typing import List, Dict
from src.infrastructure.db import cargar_historial, guardar_historial

class DBHistoryRepository:
    def cargar(self, user_id: int) -> List[Dict[str, str]]:
        return cargar_historial(user_id)
        
    def guardar(self, user_id: int, historial: List[Dict[str, str]]) -> None:
        guardar_historial(user_id, historial)
