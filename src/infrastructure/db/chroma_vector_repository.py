"""
Path: src/infrastructure/db/chroma_vector_repository.py
"""

import chromadb
from typing import List, Dict
from src.application.ports.embedding_gateway import EmbeddingGateway
from src.infrastructure.settings.logger import logger

CHROMA_DIR = "chroma_db"

class ChromaVectorRepository:
    def __init__(self, embedding_gateway: EmbeddingGateway):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.coleccion = self.client.get_or_create_collection("reglamento_f1")
        self.embedding_gateway = embedding_gateway

    def count(self) -> int:
        return self.coleccion.count()

    def count_documents(self) -> int:
        return self.count()

    def add_texts(self, textos: List[str], metadatos: List[Dict], ids: List[str]):
        embeds = self.embedding_gateway.embed_texts(textos)
        self.coleccion.add(documents=textos, embeddings=embeds, ids=ids, metadatas=metadatos)
        logger.info(f"⚡ RAG: Se sumaron {len(textos)} fragmentos.")

    def query(self, consulta: str, n_resultados: int = 5) -> Dict:
        embed = self.embedding_gateway.embed_texts([consulta])
        return self.coleccion.query(
            query_embeddings=embed,
            n_results=min(n_resultados, self.coleccion.count()),
        )
