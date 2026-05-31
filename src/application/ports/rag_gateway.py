from typing import Protocol

class RagGateway(Protocol):
    def buscar_reglamento(self, consulta: str) -> str:
        ...
