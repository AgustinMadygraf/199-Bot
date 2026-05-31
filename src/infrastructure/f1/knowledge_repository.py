"""
Path: src/infrastructure/f1/knowledge_repository.py
"""

from pathlib import Path
from src.application.ports.rag_gateway import RagGateway
from src.application.ports.live_knowledge_gateway import LiveKnowledgeGateway
from src.application.ports.tutor_ports import KnowledgeRepository

DATA_FILE = Path(__file__).resolve().parents[3] / "data" / "knowedge.md"

class F1KnowledgeRepository(KnowledgeRepository):
    def __init__(self, rag_gateway: RagGateway, live_knowledge_gateway: LiveKnowledgeGateway) -> None:
        self._rag_gateway = rag_gateway
        self._live_knowledge_gateway = live_knowledge_gateway
        self._static_knowledge = self._load_static_knowledge()

    @staticmethod
    def _load_static_knowledge() -> str:
        try:
            return DATA_FILE.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Knowledge file not found: {DATA_FILE}. Create data/knowedge.md with the F1 knowledge source."
            ) from exc

    @property
    def static_knowledge(self) -> str:
        return self._static_knowledge
        
    def buscar_reglamento(self, consulta: str) -> str:
        palabras_reglamento = [
            "reglamento", "regla", "artículo", "norma", "permitido", "prohibido",
            "sanción", "penalización", "peso", "dimensión", "motor", "combustible",
            "neumático", "alerón", "drs", "ers", "mgu", "pit", "boxes", "parc fermé",
            "bandera", "safety car", "vsc", "descalificación", "protesta"
        ]
        if any(w in consulta.lower() for w in palabras_reglamento):
            return self._rag_gateway.buscar_reglamento(consulta)
        return ""
        
    async def obtener_datos_vivos(self, consulta: str) -> str:
        return await self._live_knowledge_gateway.get_live_knowledge(consulta)
