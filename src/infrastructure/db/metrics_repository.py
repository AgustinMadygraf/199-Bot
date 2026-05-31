import sqlite3
from src.application.ports.metrics_ports import MetricsRepository

class SQLiteMetricsRepository(MetricsRepository):
    def __init__(self, db_path: str = "historial.db"):
        self.db_path = db_path

    def registrar_consulta(self, user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str) -> None:
        username_seguro = username if username else "Anónimo"
        con = sqlite3.connect(self.db_path)
        with con:
            con.execute("""
                INSERT INTO metricas_consultas (user_id, username, mensaje_usuario, tipo_respuesta)
                VALUES (?, ?, ?, ?)
            """, (user_id, username_seguro, mensaje_usuario, tipo_respuesta))
        con.close()

    def __call__(self, user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str) -> None:
        self.registrar_consulta(user_id, username, mensaje_usuario, tipo_respuesta)
