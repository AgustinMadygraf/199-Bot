"""
Path: src/infrastructure/llm/groq_client.py
"""

from groq import Groq
from groq.types.chat import ChatCompletionMessageParam
from typing import Iterable

class GroqLLMClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        
    async def generar_respuesta(self, messages: Iterable[ChatCompletionMessageParam]) -> str:
        respuesta = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        contenido = respuesta.choices[0].message.content
        if contenido is None:
            raise RuntimeError("La respuesta de Groq no contiene contenido de mensaje.")
        return contenido
