"""
Path: src/interface_adapters/controllers/command_controller.py
"""

from src.application.ports.tutor_ports import HistoryRepository
from src.infrastructure.rag_indexer import RAGIndexer

class CommandController:
    rag_service: RAGIndexer
    history_repository: HistoryRepository

    def __init__(self, rag_service: RAGIndexer, history_repository: HistoryRepository):
        self.rag_service = rag_service
        self.history_repository = history_repository

    def get_start_message(self) -> str:
        try:
            rag_count = self.rag_service.repository.count()
            rag_status = "✅ Reglamento FIA 2026 indexado" if rag_count > 0 else "⏳ Reglamento no disponible"
        except Exception:
            rag_status = "⚠️ Error al verificar base de conocimientos"

        return (
            "🏎️ **¡Bienvenido al 199-Bot!**\n\n"
            "Soy tu asistente experto en Fórmula 1, especializado en el nuevo reglamento 2026.\n\n"
            f"Estado del sistema: {rag_status}\n\n"
            "Puedes hacerme preguntas sobre:\n"
            "• Cambios en los motores 2026\n"
            "• Aerodinámica activa\n"
            "• Calendario y resultados actuales\n"
            "• ¡O poner a prueba tus conocimientos con /quiz!\n\n"
            "¿En qué puedo ayudarte hoy?"
        )
