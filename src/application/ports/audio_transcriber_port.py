from typing import Protocol

class AudioTranscriber(Protocol):
    async def transcribir(self, file_path: str) -> str:
        ...
