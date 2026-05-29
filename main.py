"""
Path: main.py
"""

from src.infrastructure.settings.config import cargar_configuracion
from src.infrastructure.settings.logger import setup_logging, logger

# 1. Configuración de entorno y logs
cargar_configuracion()
setup_logging()

# 2. Importaciones de la Arquitectura
from src.infrastructure.db import init_db, registrar_consulta
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
from src.infrastructure.adapters.tutor_adapters import GroqLLMClient, F1KnowledgeRepository, DBHistoryRepository

# 3. Inicialización de Componentes
quiz_use_case = QuizUseCase()

# Inyección de dependencias para TutorUseCase
llm_client = GroqLLMClient()
knowledge_repo = F1KnowledgeRepository()
history_repo = DBHistoryRepository()
tutor_use_case = TutorUseCase(llm_client, knowledge_repo, history_repo)

audio_service = AudioService()
chat_processor = ChatProcessorUseCase(tutor_use_case, quiz_use_case, registrar_consulta)

# Inicializamos primero el bot, y luego el SystemController que lo necesita
bot_service = TelegramBot(None, None, None) 
system_controller = SystemController(audio_service, bot_service, chat_processor, rag_service)

# Ahora inyectamos el controlador en el bot
bot_service.system_controller = system_controller
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
