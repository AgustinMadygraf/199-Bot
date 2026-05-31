"""
Path: src/application/ports/metrics_ports.py
"""

from typing import Protocol

class MetricsRepository(Protocol):
    def registrar_consulta(self, user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str) -> None:
        ...
