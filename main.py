"""
Path: main.py
"""

from typing import Any, cast
from src.infrastructure.settings.config import cargar_configuracion, obtener_groq_api_key
from src.infrastructure.settings.logger import setup_logging, logger

# 1. Configuración de entorno y logs
cargar_configuracion()
setup_logging()

# 2. Importaciones de la Arquitectura
from src.infrastructure.db import init_db
from src.infrastructure.db.history_repository import DBHistoryRepository
from src.infrastructure.f1_rag import indexar_reglamento
import src.infrastructure.f1_rag as rag_service
from src.infrastructure.audio_service import AudioService
from src.application.chat_processor import ChatProcessorUseCase
from src.application.quiz_use_case import QuizUseCase
from src.application.tutor_use_case import TutorUseCase
from src.presentation.race_controller import RaceController
from src.presentation.quiz_controller import QuizController
from src.presentation.system_controller import SystemController
from src.infrastructure.telegram.telegram_bot import TelegramBot
from src.infrastructure.llm.groq_client import GroqLLMClient
from src.infrastructure.f1.knowledge_repository import F1KnowledgeRepository
from src.infrastructure.db.history_repository import DBHistoryRepository
from src.infrastructure.random.shuffler_adapter import RandomShuffler

# 3. Inicialización de Componentes
shuffler = RandomShuffler()
quiz_use_case = QuizUseCase(shuffler)

# Inyección de dependencias para TutorUseCase
llm_client = GroqLLMClient(api_key=obtener_groq_api_key())
knowledge_repo = F1KnowledgeRepository()
history_repo = DBHistoryRepository()
tutor_use_case = TutorUseCase(llm_client, knowledge_repo, history_repo)

audio_service = AudioService()
chat_processor = ChatProcessorUseCase(tutor_use_case, quiz_use_case, history_repo.registrar_consulta)

# Inicializamos primero el bot, y luego el SystemController que lo necesita
bot_service = TelegramBot(None, None, None) 
system_controller = SystemController(audio_service, bot_service, chat_processor, rag_service)

# Ahora inyectamos el controlador en el bot
# Bypass static type restrictions on attribute assignment when wiring controllers
cast(Any, bot_service).system_controller = system_controller
bot_service.race_controller = RaceController()
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
