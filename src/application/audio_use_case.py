"""
Path: src/application/audio_use_case.py
"""

import os
from src.application.ports.audio_gateway import AudioGateway

class AudioUseCase:
    def __init__(self, audio_gateway: AudioGateway):
        self.audio_gateway = audio_gateway

    async def transcribir(self, file_path: str) -> str:
        try:
            texto = await self.audio_gateway.transcribir_ogg(file_path)
            return texto
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
