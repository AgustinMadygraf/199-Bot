"""
Path: src/application/ports/query_registrar.py
"""

from typing import Protocol

class QueryRegistrar(Protocol):
    """Interfaz para registrar consultas en el sistema de persistencia."""
    def __call__(self, user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str) -> None:
        ...
