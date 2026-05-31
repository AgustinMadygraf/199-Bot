"""
Path: src/application/quiz_use_case.py
"""

from typing import Dict, Optional, Tuple
from src.domain.entities.quiz import QuizSession, Pregunta
from src.domain.services.shuffler import ListShuffler
from src.application.ports.quiz_ports import QuizRepository

class QuizUseCase:
    def __init__(self, shuffler: ListShuffler, quiz_repo: QuizRepository):
        self.sesiones: Dict[int, QuizSession] = {}
        self.shuffler = shuffler
        self.quiz_repo = quiz_repo

    def iniciar_quiz(self, user_id: int, dificultad: str) -> Optional[Pregunta]:
        preguntas = self.quiz_repo.obtener_preguntas(dificultad)
        if not preguntas:
            return None
            
        self.sesiones[user_id] = QuizSession(dificultad, preguntas, self.shuffler)
        return self.sesiones[user_id].obtener_pregunta_actual()
    
    def esta_jugando(self, user_id: int) -> bool:
        return user_id in self.sesiones and not self.sesiones[user_id].pregunta_terminada

    def responder(self, user_id: int, respuesta: str) -> Tuple[bool, Pregunta, bool, Optional[int], Optional[int]]:
        session: Optional[QuizSession] = self.sesiones.get(user_id)
        if not session:
            raise ValueError("No hay ninguna sesión de quiz activa.")
            
        es_correcta, pregunta = session.procesar_respuesta(respuesta)
        
        if session.pregunta_terminada:
            puntaje = session.puntaje
            total = session.total_preguntas
            del self.sesiones[user_id]
            return es_correcta, pregunta, True, puntaje, total
            
        return es_correcta, pregunta, False, None, None
