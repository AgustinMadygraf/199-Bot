"""
Path: main.py
"""

from typing import Any, cast
from src.infrastructure.settings.config import (
    cargar_configuracion, 
    obtener_groq_api_key,
    obtener_llm_provider,
    obtener_llm_model,
    obtener_llm_temperature
)
from src.infrastructure.settings.logger import setup_logging, logger

# 1. Configuración de entorno y logs
cargar_configuracion()
setup_logging()

# 2. Importaciones de la Arquitectura
from src.infrastructure.db.sqlite_handler import init_db
from src.infrastructure.db.metrics_repository import SQLiteMetricsRepository
from src.infrastructure.db.history_repository import SQLiteHistoryRepository
from src.infrastructure.audio_service import AudioService
from src.application.audio_use_case import AudioUseCase
from src.application.chat_processor import ChatProcessorUseCase
from src.application.quiz_use_case import QuizUseCase
from src.application.tutor_use_case import TutorUseCase
from src.presentation.race_controller import RaceController
from src.infrastructure.f1_api_gateway import F1ApiGateway
from src.presentation.quiz_controller import QuizController
from src.presentation.system_controller import SystemController
from src.infrastructure.telegram.telegram_bot import TelegramBot
from src.infrastructure.llm.groq_client import GroqLLMClient
from src.infrastructure.f1.knowledge_repository import F1KnowledgeRepository
from src.infrastructure.f1.prompt_repository import FilePromptRepository
from src.infrastructure.f1_rag_gateway import F1RagGateway
from src.infrastructure.f1_live_knowledge_gateway import F1LiveKnowledgeGateway
from src.infrastructure.random.shuffler_adapter import RandomShuffler
from src.infrastructure.quiz.json_quiz_repository import JsonQuizRepository
from src.infrastructure.chroma_db_repository import ChromaDBRepository
from src.infrastructure.pdf_service import PDFService
from src.infrastructure.rag_indexer import RAGIndexer

# 3. Inicialización de Componentes
shuffler = RandomShuffler()
f1_gateway = F1ApiGateway()
chroma_repo = ChromaDBRepository()
pdf_service = PDFService()
indexer = RAGIndexer(chroma_repo, pdf_service)
quiz_repo = JsonQuizRepository(data_path="data/quiz/preguntas.json")
quiz_use_case = QuizUseCase(shuffler, quiz_repo)

# Inyección de dependencias para TutorUseCase
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

audio_service = AudioService()
audio_use_case = AudioUseCase(audio_service)
chat_processor = ChatProcessorUseCase(tutor_use_case, quiz_use_case, SQLiteMetricsRepository())

# Inicializamos primero el bot, y luego el SystemController que lo necesita
bot_service = TelegramBot(None, None, None) 
system_controller = SystemController(audio_use_case, bot_service, chat_processor, None, history_repo)

# Ahora inyectamos el controlador en el bot
cast(Any, bot_service).system_controller = system_controller
bot_service.race_controller = RaceController(f1_gateway)
bot_service.quiz_controller = QuizController(quiz_use_case)

def main():
    # Inicialización física de recursos de datos e IA
    init_db()
    
    logger.info("📚 Preparando sistema...")
    indexer.indexar()
    
    # Encender el bot
    logger.info("🚀 Motor encendido: F1 Tutor Bot listo en Telegram.")
    bot_service.encender()

if __name__ == "__main__":
    main()
