import os
from groq import Groq
from src.application.ports.audio_gateway import AudioGateway

class GroqAudioTranscriber:
    """Implementación de infraestructura para la transcripción de audio mediante Whisper en Groq."""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    async def transcribir_ogg(self, file_path: str) -> str:
        """Toma un archivo local en formato .ogg y devuelve su transcripción en texto."""
        with open(file_path, "rb") as f:
            transcripcion = self.client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f,
                language="es",
            )
        return transcripcion.text
