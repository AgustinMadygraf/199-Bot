from typing import Protocol, Iterable
from groq.types.chat import ChatCompletionMessageParam

class LLMClient(Protocol):
    async def generar_respuesta(self, messages: Iterable[ChatCompletionMessageParam]) -> str:
        ...

class KnowledgeRepository(Protocol):
    def buscar_reglamento(self, consulta: str) -> str:
        ...
    async def obtener_datos_vivos(self, consulta: str) -> str:
        ...
    @property
    def static_knowledge(self) -> str:
        ...

class HistoryRepository(Protocol):
    def cargar(self, user_id: int) -> List[Dict[str, str]]:
        ...
    def guardar(self, user_id: int, historial: List[Dict[str, str]]) -> None:
        ...
