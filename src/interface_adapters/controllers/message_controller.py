"""
Path: src/interface_adapters/controllers/message_controller.py
"""

from src.application.message_orchestrator import MessageOrchestrator
from src.application.audio_use_case import AudioUseCase
from typing import Optional, List

class MessageController:
    def __init__(self, message_orchestrator: MessageOrchestrator, audio_use_case: AudioUseCase):
        self.message_orchestrator = message_orchestrator
        self.audio_use_case = audio_use_case

    async def procesar_mensaje(self, user_id: int, username: str, texto: str) -> List[str]:
        # Retorna lista de fragmentos para enviar
        respuesta = await self.message_orchestrator.procesar_mensaje(user_id, username, texto)
        return [respuesta[i:i + 4096] for i in range(0, len(respuesta), 4096)]

    async def procesar_audio(self, user_id: int, username: str, file_path: str) -> Optional[str]:
        texto_transcrito = await self.audio_use_case.transcribir(file_path)
        if not texto_transcrito:
            return None
        
        respuesta = await self.message_orchestrator.procesar_mensaje(user_id, username, texto_transcrito)
        return f"🎤 *Entendido:* _{texto_transcrito}_\n\n{respuesta}"
