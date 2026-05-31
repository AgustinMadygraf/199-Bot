"""
Path: src/application/quiz_use_case.py
"""

from typing import Dict, Optional
from src.domain.entities.quiz import QuizSession
from src.domain.services.shuffler import ListShuffler
from src.application.ports.quiz_ports import QuizRepository

class QuizUseCase:
    def __init__(self, shuffler: ListShuffler, quiz_repo: QuizRepository):
        self.sesiones: Dict[int, QuizSession] = {}
        self.shuffler = shuffler
        self.quiz_repo = quiz_repo

    def iniciar_quiz(self, user_id: int, dificultad: str) -> str:
        preguntas = self.quiz_repo.obtener_preguntas(dificultad)
        if not preguntas:
            return "No hay preguntas disponibles para esa dificultad."
            
        self.sesiones[user_id] = QuizSession(dificultad, preguntas, self.shuffler)
        
        proxima = self.sesiones[user_id].obtener_pregunta_actual()
        return f"¡Juego iniciado! {proxima.texto}\nOpciones: {', '.join(proxima.opciones)}"
    
    def esta_jugando(self, user_id: int) -> bool:
        return user_id in self.sesiones and not self.sesiones[user_id].pregunta_terminada

    def responder(self, user_id: int, respuesta: str) -> str:
        session: Optional[QuizSession] = self.sesiones.get(user_id)
        if not session:
            return "No hay ninguna sesión de quiz activa."
            
        es_correcta, pregunta = session.procesar_respuesta(respuesta)
        
        resultado_txt = "✅ ¡Correcto!" if es_correcta else f"❌ Incorrecto. La respuesta era {pregunta.respuesta_correcta}."
        
        if session.pregunta_terminada:
            puntaje = session.puntaje
            total = session.total_preguntas
            del self.sesiones[user_id]
            return f"{resultado_txt}\n\nQuiz finalizado. Puntaje: {puntaje}/{total}."
            
        proxima = session.obtener_pregunta_actual()
        return f"{resultado_txt}\n\nSiguiente: {proxima.texto}\nOpciones: {', '.join(proxima.opciones)}"
