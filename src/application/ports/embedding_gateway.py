"""
Path: src/application/ports/embedding_gateway.py
"""

from typing import Protocol, List

class EmbeddingGateway(Protocol):
    def embed_texts(self, textos: List[str]) -> List[List[float]]:
        ...
