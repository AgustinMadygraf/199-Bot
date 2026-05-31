from src.application.ports.rag_gateway import RagGateway
import src.infrastructure.f1_rag as f1_rag

class F1RagGateway(RagGateway):
    def buscar_reglamento(self, consulta: str) -> str:
        # Se asume que f1_rag.buscar_reglamento retorna un string
        resultado: str = f1_rag.buscar_reglamento(consulta)
        return resultado
