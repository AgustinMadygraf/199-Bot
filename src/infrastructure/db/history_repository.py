"""
Path: src/infrastructure/db/history_repository.py
"""

import json
from typing import List, Dict, Any
from src.infrastructure.db import cargar_historial, guardar_historial
from src.domain.entities.chat_message import ChatMessage
from src.application.ports.tutor_ports import HistoryRepository # Import the protocol for explicit implementation

class DBHistoryRepository(HistoryRepository): # Explicitly implement the protocol
    def cargar(self, user_id: int) -> List[ChatMessage]:
        # Load raw dictionaries and convert them to ChatMessage objects
        raw_historial: List[Dict[str, Any]] = cargar_historial(user_id)
        return [ChatMessage(role=msg["role"], content=msg["content"]) for msg in raw_historial]
        
    def guardar(self, user_id: int, historial: List[ChatMessage]) -> None:
        # Convert ChatMessage objects to dictionaries before saving
        raw_historial: List[Dict[str, Any]] = [{"role": msg.role, "content": msg.content} for msg in historial]
        guardar_historial(user_id, raw_historial)
