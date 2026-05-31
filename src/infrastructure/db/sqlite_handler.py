"""Database utilities for SQLite storage in the infrastructure layer."""

import sqlite3

DB_PATH = "historial.db"

def init_db() -> None:
    """Crea la base de datos y las tablas de historial y métricas si no existen."""
    con = sqlite3.connect(DB_PATH)
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                user_id     INTEGER PRIMARY KEY,
                mensajes    TEXT    NOT NULL DEFAULT '[]',
                actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS metricas_consultas (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id          INTEGER NOT NULL,
                username         TEXT,
                mensaje_usuario  TEXT    NOT NULL,
                tipo_respuesta   TEXT    NOT NULL,
                fecha_hora       TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
    con.close()
