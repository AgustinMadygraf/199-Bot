"""
Path: src/application/message_orchestrator.py
"""

from src.application.chat_processor import ChatProcessorUseCase
from src.interface_adapters.controllers.quiz_controller import QuizController

class MessageOrchestrator:
    chat_processor: ChatProcessorUseCase
    quiz_controller: QuizController

    def __init__(self, chat_processor: ChatProcessorUseCase, quiz_controller: QuizController):
        self.chat_processor = chat_processor
        self.quiz_controller = quiz_controller

    async def procesar_mensaje(self, user_id: int, username: str, texto: str) -> str:
        if self.quiz_controller and self.quiz_controller.quiz_use_case.esta_jugando(user_id):
            return await self.quiz_controller.responder(user_id, texto)
        else:
            return await self.chat_processor.procesar(user_id, username, texto, "consulta_general")
