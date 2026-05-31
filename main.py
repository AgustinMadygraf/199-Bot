"""
Path: main.py
"""

from src.infrastructure.settings.config import (
    cargar_configuracion, 
    obtener_groq_api_key,
    obtener_llm_provider,
    obtener_llm_model,
    obtener_llm_temperature
)
from src.infrastructure.settings.logger import setup_logging, logger

cargar_configuracion()
setup_logging()

from src.infrastructure.db.sqlite_handler import init_db
from src.infrastructure.db.metrics_repository import SQLiteMetricsRepository
from src.infrastructure.db.history_repository import SQLiteHistoryRepository
from src.infrastructure.groq_audio_transcriber import GroqAudioTranscriber
from src.application.audio_use_case import AudioUseCase
from src.application.chat_processor import ChatProcessorUseCase
from src.application.quiz_use_case import QuizUseCase
from src.application.tutor_use_case import TutorUseCase
from src.application.f1_use_case import F1UseCase
from src.interface_adapters.controllers.f1_controller import F1Controller
from src.interface_adapters.presenters.f1_formatter import F1Formatter
from src.infrastructure.f1_api_gateway import F1ApiGateway
from src.interface_adapters.controllers.quiz_controller import QuizController
from src.interface_adapters.presenters.quiz_formatter import QuizFormatter
from src.application.message_orchestrator import MessageOrchestrator
from src.interface_adapters.controllers.command_controller import CommandController
from src.interface_adapters.controllers.message_controller import MessageController
from src.infrastructure.telegram.telegram_bot import TelegramBot
from src.infrastructure.telegram.controller_registry import ControllerRegistry
from src.infrastructure.llm.groq_client import GroqLLMClient
from src.infrastructure.f1.knowledge_repository import F1KnowledgeRepository
from src.infrastructure.f1.prompt_repository import FilePromptRepository
from src.infrastructure.f1_rag_gateway import F1RagGateway
from src.infrastructure.f1_live_knowledge_gateway import F1LiveKnowledgeGateway
from src.infrastructure.random.shuffler_adapter import RandomShuffler
from src.infrastructure.quiz.json_quiz_repository import JsonQuizRepository
from src.infrastructure.chroma_db_status_adapter import ChromaDBStatusAdapter
from src.infrastructure.db.chroma_vector_repository import ChromaVectorRepository
from src.infrastructure.embeddings.sentence_transformer_service import SentenceTransformerService
from src.infrastructure.pdf_service import PDFService
from src.infrastructure.rag_indexer import RAGIndexer

shuffler = RandomShuffler()
f1_gateway = F1ApiGateway()
embedding_service = SentenceTransformerService()
chroma_repo = ChromaVectorRepository(embedding_service)
pdf_service = PDFService()
indexer = RAGIndexer(chroma_repo, pdf_service)
chroma_status_adapter = ChromaDBStatusAdapter(chroma_repo)
quiz_repo = JsonQuizRepository(data_path="data/quiz/preguntas.json")
quiz_formatter = QuizFormatter()
quiz_use_case = QuizUseCase(shuffler, quiz_repo)

llm_provider = obtener_llm_provider()
if llm_provider == "groq":
    llm_client = GroqLLMClient(
        api_key=obtener_groq_api_key(),
        model=obtener_llm_model(),
        temperature=obtener_llm_temperature()
    )
else:
    raise ValueError(f"Proveedor de LLM no soportado: {llm_provider}")

knowledge_repo = F1KnowledgeRepository(F1RagGateway(chroma_repo), F1LiveKnowledgeGateway(f1_gateway))
history_repo = SQLiteHistoryRepository()
prompt_repo = FilePromptRepository()
tutor_use_case = TutorUseCase(llm_client, knowledge_repo, history_repo, prompt_repo)

audio_service = GroqAudioTranscriber(obtener_groq_api_key())
audio_use_case = AudioUseCase(audio_service)
chat_processor = ChatProcessorUseCase(tutor_use_case, quiz_use_case, SQLiteMetricsRepository())

registry = ControllerRegistry()

quiz_controller = QuizController(quiz_use_case, quiz_formatter)
f1_use_case = F1UseCase(f1_gateway)
f1_formatter = F1Formatter()
f1_controller = F1Controller(f1_use_case, f1_formatter)
message_orchestrator = MessageOrchestrator(chat_processor, quiz_controller)
command_controller = CommandController(chroma_status_adapter, history_repo)
message_controller = MessageController(message_orchestrator, audio_use_case)


registry.register("command", command_controller)
registry.register("message", message_controller)
registry.register("race", f1_controller)
registry.register("quiz", quiz_controller)

# Inicializamos el bot con el registry
bot_service = TelegramBot(registry)

def main():
    init_db()
    logger.info("📚 Preparando sistema...")
    indexer.indexar()
    logger.info("🚀 Motor encendido: F1 Tutor Bot listo en Telegram.")
    bot_service.encender()

if __name__ == "__main__":
    main()
