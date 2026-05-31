from src.application.ports.live_knowledge_gateway import LiveKnowledgeGateway
from src.infrastructure.f1_api_gateway import F1ApiGateway

class F1LiveKnowledgeGateway(LiveKnowledgeGateway):
    def __init__(self, f1_gateway: F1ApiGateway) -> None:
        self._f1_gateway = f1_gateway

    async def get_live_knowledge(self, consulta: str) -> str:
        # Por ahora es un stub que preserva la funcionalidad antigua.
        # F1ApiGateway.get_last_race_results retorna un Optional[RaceResult],
        # necesitamos convertirlo a str para cumplir con el protocolo.
        resultado = await self._f1_gateway.get_last_race_results()
        return str(resultado) if resultado else "No hay datos disponibles."
