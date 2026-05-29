import os
from groq import Groq
from typing import List, Dict
from src.infrastructure.f1_knowledge import F1_STATIC_KNOWLEDGE
from src.infrastructure.db import cargar_historial, guardar_historial
from src.infrastructure.f1_api import get_relevant_f1_data
from src.infrastructure.f1_rag import buscar_reglamento

class GroqLLMClient:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
    async def generar_respuesta(self, messages: List[Dict[str, str]]) -> str:
        respuesta = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return respuesta.choices[0].message.content

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
        # Ahora correctamente asíncrono
        return await get_relevant_f1_data(consulta)

class DBHistoryRepository:
    def cargar(self, user_id: int) -> List[Dict[str, str]]:
        return cargar_historial(user_id)
        
    def guardar(self, user_id: int, historial: List[Dict[str, str]]) -> None:
        guardar_historial(user_id, historial)
