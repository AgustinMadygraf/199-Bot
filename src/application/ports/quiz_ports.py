from typing import Protocol, List
from src.domain.entities.quiz import Pregunta

class QuizRepository(Protocol):
    def obtener_preguntas(self, dificultad: str) -> List[Pregunta]:
        """Obtiene el conjunto de preguntas para una dificultad específica."""
        ...
