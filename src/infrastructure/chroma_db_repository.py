import chromadb
from sentence_transformers import SentenceTransformer
from src.infrastructure.settings.logger import logger

CHROMA_DIR = "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

class ChromaDBRepository:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.coleccion = self.client.get_or_create_collection("reglamento_f1")
        self._modelo = SentenceTransformer(EMBED_MODEL)

    def count(self) -> int:
        return self.coleccion.count()

    def add_texts(self, textos: list[str], metadatos: list[dict], ids: list[str]):
        embeds = self._modelo.encode(textos).tolist()
        self.coleccion.add(documents=textos, embeddings=embeds, ids=ids, metadatas=metadatos)
        logger.info(f"⚡ RAG: Se sumaron {len(textos)} fragmentos.")

    def query(self, consulta: str, n_resultados: int = 5) -> dict:
        embed = self._modelo.encode([consulta]).tolist()
        return self.coleccion.query(
            query_embeddings=embed,
            n_results=min(n_resultados, self.coleccion.count()),
        )
