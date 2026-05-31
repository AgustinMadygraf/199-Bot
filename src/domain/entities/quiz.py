from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.services.shuffler import ListShuffler

@dataclass(frozen=True)
class Pregunta:
    texto: str
    opciones: List[str]
    respuesta_correcta: str  # 'A', 'B', 'C' o 'D'
    explicacion: str

class QuizSession:
    def __init__(self, dificultad: str, preguntas: List[Pregunta], shuffler: 'ListShuffler'):
        self.dificultad = dificultad
        self.preguntas = shuffler.shuffle(preguntas)
        self.pregunta_actual = 0
        self.puntaje = 0
        self.total_preguntas = len(self.preguntas)
        self.pregunta_terminada = False
        self.preguntas_respondidas = 0

    def obtener_pregunta_actual(self) -> Pregunta:
        return self.preguntas[self.pregunta_actual]

    def procesar_respuesta(self, respuesta: str) -> tuple[bool, Pregunta]:
        pregunta = self.obtener_pregunta_actual()
        es_correcta = respuesta.upper() == pregunta.respuesta_correcta
        if es_correcta:
            self.puntaje += 1
        
        self.pregunta_actual += 1
        self.preguntas_respondidas += 1
        
        if self.preguntas_respondidas >= 5 or self.pregunta_actual >= self.total_preguntas:
            self.pregunta_terminada = True
            
        return es_correcta, pregunta
