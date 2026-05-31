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
from src.infrastructure.db.sqlite_handler import init_db, registrar_consulta
from src.infrastructure.db.history_repository import DBHistoryRepository
from src.infrastructure.f1_rag import indexar_reglamento
import src.infrastructure.f1_rag as rag_service
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
from src.infrastructure.f1_rag_gateway import F1RagGateway
from src.infrastructure.f1_live_knowledge_gateway import F1LiveKnowledgeGateway
from src.infrastructure.random.shuffler_adapter import RandomShuffler

# 3. Inicialización de Componentes
shuffler = RandomShuffler()
f1_gateway = F1ApiGateway()
quiz_use_case = QuizUseCase(shuffler)

# Inyección de dependencias para TutorUseCase
llm_provider = obtener_llm_provider()
if llm_provider == "groq":
    llm_client = GroqLLMClient(
        api_key=obtener_groq_api_key(),
        model=obtener_llm_model(),
        temperature=obtener_llm_temperature()
    )
else:
    # Aquí se podrían añadir otros proveedores (OpenAI, Anthropic, etc.)
    # Por ahora lanzamos error si el provider no está soportado
    raise ValueError(f"Proveedor de LLM no soportado: {llm_provider}")

knowledge_repo = F1KnowledgeRepository(F1RagGateway(), F1LiveKnowledgeGateway(f1_gateway))
history_repo = DBHistoryRepository()
tutor_use_case = TutorUseCase(llm_client, knowledge_repo, history_repo)

audio_service = AudioService()
audio_use_case = AudioUseCase(audio_service)
chat_processor = ChatProcessorUseCase(tutor_use_case, quiz_use_case, registrar_consulta)

# Inicializamos primero el bot, y luego el SystemController que lo necesita
bot_service = TelegramBot(None, None, None) 
system_controller = SystemController(audio_use_case, bot_service, chat_processor, rag_service, history_repo)

# Ahora inyectamos el controlador en el bot
# Bypass static type restrictions on attribute assignment when wiring controllers
cast(Any, bot_service).system_controller = system_controller
bot_service.race_controller = RaceController(f1_gateway)
bot_service.race_controller = RaceController(f1_gateway)
bot_service.quiz_controller = QuizController(quiz_use_case)

def main():
    # Inicialización física de recursos de datos e IA
    init_db()
    
    logger.info("📚 Indexando reglamento FIA 2026 y preparando sistema...")
    # Esto indexa los PDFs de la carpeta 'reglamento_pdfs'
    indexar_reglamento()

    # Encender el bot
    logger.info("🚀 Motor encendido: F1 Tutor Bot listo en Telegram.")
    bot_service.encender()

if __name__ == "__main__":
    main()
