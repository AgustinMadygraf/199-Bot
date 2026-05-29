"""
Path: src/infrastructure/f1/knowledge_repository.py
"""

from pathlib import Path
from src.infrastructure.f1_api import get_relevant_f1_data
from src.infrastructure.f1_rag import buscar_reglamento

DATA_FILE = Path(__file__).resolve().parents[3] / "data" / "knowedge.md"

class F1KnowledgeRepository:
    def __init__(self) -> None:
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
            return buscar_reglamento(consulta)
        return ""
        
    async def obtener_datos_vivos(self, consulta: str) -> str:
        return await get_relevant_f1_data(consulta)
