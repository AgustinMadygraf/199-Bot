from src.domain.entities.quiz import QuizSession
from src.domain.services.shuffler import ListShuffler

class QuizUseCase:
    def __init__(self, shuffler: ListShuffler):
        self.sesiones = {}
        self.shuffler = shuffler

    def iniciar_quiz(self, user_id: int, dificultad: str):
        self.sesiones[user_id] = QuizSession(dificultad, self.shuffler)
    
    def esta_jugando(self, user_id: int) -> bool:
        return user_id in self.sesiones and not self.sesiones[user_id].pregunta_terminada

    def responder(self, user_id: int, respuesta: str) -> str:
        session = self.sesiones.get(user_id)
        if not session:
            return "No hay ninguna sesión de quiz activa."
            
        es_correcta, pregunta = session.procesar_respuesta(respuesta)
        
        resultado_txt = "✅ ¡Correcto!" if es_correcta else f"❌ Incorrecto. La respuesta era {pregunta['r']}."
        
        if session.pregunta_terminada:
            puntaje = session.puntaje
            total = session.total_preguntas
            del self.sesiones[user_id]
            return f"{resultado_txt}\n\nQuiz finalizado. Puntaje: {puntaje}/{total}."
            
        proxima = session.obtener_pregunta_actual()
        return f"{resultado_txt}\n\nSiguiente: {proxima['p']}\nOpciones: {', '.join(proxima['ops'])}"
