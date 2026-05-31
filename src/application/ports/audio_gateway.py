"""
Path: src/application/ports/audio_gateway.py
"""

from typing import Protocol

class AudioGateway(Protocol):
    async def transcribir_ogg(self, file_path: str) -> str:
        ...
