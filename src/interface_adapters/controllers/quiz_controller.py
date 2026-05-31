"""
Path: src/interface_adapters/controllers/quiz_controller.py
"""

from src.application.quiz_use_case import QuizUseCase
from src.interface_adapters.presenters.quiz_formatter import QuizFormatter

class QuizController:
    def __init__(self, quiz_use_case: QuizUseCase, formatter: QuizFormatter):
        self.quiz_use_case = quiz_use_case
        self.formatter = formatter

    async def cmd_quiz(self) -> str:
        return self.formatter.formatear_menu_dificultad()

    async def iniciar_dificultad(self, user_id: int, dificultad: str) -> str:
        pregunta = self.quiz_use_case.iniciar_quiz(user_id, dificultad)
        if not pregunta:
            return "No hay preguntas disponibles."
        
        return self.formatter.formatear_pregunta(dificultad, pregunta)

    async def responder(self, user_id: int, respuesta: str) -> str:
        try:
            es_correcta, pregunta_respondida, finalizado, puntaje, total = self.quiz_use_case.responder(user_id, respuesta)

            texto_resultado = self.formatter.formatear_resultado(
                es_correcta, 
                pregunta_respondida.respuesta_correcta, 
                finalizado, 
                puntaje if puntaje is not None else 0, 
                total if total is not None else 0
            )

            if not finalizado:
                session = self.quiz_use_case.sesiones[user_id]
                pregunta_siguiente = session.obtener_pregunta_actual()
                dificultad = session.dificultad
                texto_respuesta = self.formatter.formatear_pregunta(dificultad, pregunta_siguiente, texto_resultado)
            else:
                texto_respuesta = texto_resultado
                
            return texto_respuesta
            
        except ValueError as e:
            return str(e)

    async def cmd_facil(self, user_id: int) -> str:
        return await self.iniciar_dificultad(user_id, "facil")

    async def cmd_medio(self, user_id: int) -> str:
        return await self.iniciar_dificultad(user_id, "medio")

    async def cmd_dificil(self, user_id: int) -> str:
        return await self.iniciar_dificultad(user_id, "dificil")
