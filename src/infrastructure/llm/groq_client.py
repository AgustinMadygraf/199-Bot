"""
Path: src/infrastructure/llm/groq_client.py
"""

from groq import AsyncGroq
from groq.types.chat import ChatCompletionMessageParam # Keep this for internal conversion
from typing import Iterable, cast
from src.application.ports.tutor_ports import LLMClient
from src.domain.entities.chat_message import ChatMessage

class GroqLLMClient(LLMClient):
    def __init__(
        self, 
        api_key: str, 
        model: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ):
        self.client = AsyncGroq(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    async def generar_respuesta(self, messages: Iterable[ChatMessage]) -> str:
        # Convert domain ChatMessage objects to Groq's ChatCompletionMessageParam
        groq_messages = cast(
            list[ChatCompletionMessageParam],
            [{"role": msg.role, "content": msg.content} for msg in messages]
        )
        respuesta = await self.client.chat.completions.create(
            model=self.model,
            messages=groq_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        contenido = respuesta.choices[0].message.content
        if contenido is None:
            raise RuntimeError("La respuesta de Groq no contiene contenido de mensaje.")
        return contenido
