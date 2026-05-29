"""
main.py — Bot educativo de F1
Punto de entrada agnóstico e inicialización general del sistema.
"""

from src.infrastructure.settings.config import cargar_configuracion
from src.infrastructure.settings.logger import setup_logging, info
from src.infrastructure.db import init_db
from src.infrastructure.f1_rag import indexar_reglamento
from src.infrastructure.audio_service import AudioService
from src.infrastructure.telegram_bot import TelegramBot
from src.presentation.race_controller import RaceController
from src.presentation.quiz_controller import QuizController
from src.presentation.system_controller import SystemController
from src.use_cases.quiz_use_case import QuizUseCase
from src.use_cases.tutor_use_case import TutorUseCase

cargar_configuracion()
setup_logging()

quiz_use_case = QuizUseCase()
tutor_use_case = TutorUseCase()
audio_service = AudioService()

race_controller = RaceController()
quiz_controller = QuizController(quiz_use_case)
system_controller = SystemController(tutor_use_case, quiz_use_case, audio_service)

bot_service = TelegramBot(system_controller, race_controller, quiz_controller)

def main():
    init_db()
    info("📚 Indexando reglamento FIA 2026 y preparando sistema...")
    indexar_reglamento()
    info("🚀 Motor encendido: F1 Tutor Bot listo en Telegram.")
    bot_service.encender()

if __name__ == "__main__":
    main()
