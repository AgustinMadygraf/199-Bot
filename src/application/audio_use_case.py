"""
Path: src/application/audio_use_case.py
"""

import os
from src.infrastructure.audio_service import AudioService

class AudioUseCase:
    """Caso de uso para gestionar la transcripción de audio."""
    
    def __init__(self, audio_service: AudioService):
        self.audio_service = audio_service

    async def transcribir(self, file_path: str) -> str:
        """Transcribe un archivo de audio y asegura su limpieza posterior."""
        try:
            texto = await self.audio_service.transcribir_ogg(file_path)
            return texto
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
