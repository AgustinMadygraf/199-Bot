import json
from typing import List
from pathlib import Path
from src.domain.entities.quiz import Pregunta
from src.application.ports.quiz_ports import QuizRepository

class JsonQuizRepository(QuizRepository):
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def obtener_preguntas(self, dificultad: str) -> List[Pregunta]:
        if not self.data_path.exists():
            return []
            
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        preguntas_raw = data.get(dificultad, [])
        return [Pregunta(**p) for p in preguntas_raw]
