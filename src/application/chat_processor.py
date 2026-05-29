"""
Path: src/application/chat_processor.py
"""

from src.application.ports.query_registrar import QueryRegistrar

class ChatProcessorUseCase:
    """Caso de uso para procesar consultas de chat (texto o audio transcrito)."""
    
    def __init__(self, tutor_use_case, quiz_use_case, query_registrar: QueryRegistrar):
        self.tutor_use_case = tutor_use_case
        self.quiz_use_case = quiz_use_case
        self.query_registrar = query_registrar

    async def procesar(self, user_id: int, username: str, texto: str, tipo_consulta: str) -> str:
        """Procesa el texto (ya sea directo o transcrito de audio) y devuelve la respuesta."""
        
        # 1. Si está en un quiz, responder directamente
        if self.quiz_use_case.esta_jugando(user_id):
            resultado = self.quiz_use_case.responder(user_id, texto)
            self.query_registrar(user_id, username, texto, "quiz_respuesta")
            return resultado

        # 2. Si es una consulta general, usar el tutor
        respuesta = await self.tutor_use_case.ejecutar_consulta(user_id, texto)
        self.query_registrar(user_id, username, texto, tipo_consulta)
        
        return respuesta
