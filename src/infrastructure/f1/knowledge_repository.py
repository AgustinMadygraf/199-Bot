"""
Path: src/infrastructure/f1/knowledge_repository.py
"""

from src.infrastructure.f1_knowledge import F1_STATIC_KNOWLEDGE
from src.infrastructure.f1_api import get_relevant_f1_data
from src.infrastructure.f1_rag import buscar_reglamento

class F1KnowledgeRepository:
    @property
    def static_knowledge(self) -> str:
        return F1_STATIC_KNOWLEDGE
        
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
