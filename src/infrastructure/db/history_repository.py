import sqlite3
import json
from typing import List
from src.domain.entities.chat_message import ChatMessage
from src.application.ports.tutor_ports import HistoryRepository

class SQLiteHistoryRepository(HistoryRepository):
    def __init__(self, db_path: str = "historial.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def cargar(self, user_id: int) -> List[ChatMessage]:
        con = self._connect()
        row = con.execute(
            "SELECT mensajes FROM historial WHERE user_id = ?", (user_id,)
        ).fetchone()
        con.close()

        if row:
            raw_data = json.loads(row[0])
            return [ChatMessage(role=msg["role"], content=msg["content"]) for msg in raw_data]
        return []

    def guardar(self, user_id: int, historial: List[ChatMessage]) -> None:
        raw_historial = [{"role": msg.role, "content": msg.content} for msg in historial]
        con = self._connect()
        with con:
            con.execute("""
                INSERT INTO historial (user_id, mensajes, actualizado)
                VALUES (?, ?, datetime('now'))
                ON CONFLICT(user_id) DO UPDATE SET
                    mensajes    = excluded.mensajes,
                    actualizado = excluded.actualizado
            """, (user_id, json.dumps(raw_historial, ensure_ascii=False)))
        con.close()

    def borrar(self, user_id: int) -> None:
        con = self._connect()
        with con:
            con.execute("DELETE FROM historial WHERE user_id = ?", (user_id,))
        con.close()
