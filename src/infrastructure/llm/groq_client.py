"""
Path: src/infrastructure/llm/groq_client.py
"""

import os
from groq import Groq
from typing import List, Dict

class GroqLLMClient:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
    async def generar_respuesta(self, messages: List[Dict[str, str]]) -> str:
        respuesta = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return respuesta.choices[0].message.content
