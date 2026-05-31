"""
Path: src/infrastructure/embeddings/sentence_transformer_service.py
"""

from typing import List
from sentence_transformers import SentenceTransformer
from src.application.ports.embedding_gateway import EmbeddingGateway

class SentenceTransformerService(EmbeddingGateway):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._modelo = SentenceTransformer(model_name)

    def embed_texts(self, textos: List[str]) -> List[List[float]]:
        return self._modelo.encode(textos).tolist()
