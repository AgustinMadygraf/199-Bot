# src/infrastructure/telegram/telegram_bot.py
import time
from typing import Any, Optional, TYPE_CHECKING
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from src.infrastructure.settings.config import obtener_token_telegram, obtener_tiempo_minimo_consulta
from src.infrastructure.settings.logger import logger

if TYPE_CHECKING:
    from src.presentation.race_controller import RaceController
    from src.presentation.quiz_controller import QuizController
    from src.presentation.system_controller import SystemController

class TelegramBot:
    """Encapsula la infraestructura específica de Telegram para aislar el main.py."""
    
    def __init__(
        self,
        system_controller: Optional["SystemController"],
        race_controller: Optional["RaceController"],
        quiz_controller: Optional["QuizController"],
    ):
        # El token se lee a través del módulo de configuración
        self.token = obtener_token_telegram()
            
        self.system_controller = system_controller
        self.race_controller = race_controller
        self.quiz_controller = quiz_controller
        self.app: Optional[Any] = None
        
        # 🔐 Memoria volátil para el Rate Limiting (user_id: timestamp_ultimo_mensaje)
        self._ultimas_consultas = {}
        self._TIEMPO_MINIMO = obtener_tiempo_minimo_consulta()

    def es_spammer(self, user_id: int) -> bool:
        """🔐 Verifica si el usuario está enviando mensajes demasiado rápido."""
        ahora = time.time()
        ultimo_registro = self._ultimas_consultas.get(user_id, 0)
        
        if ahora - ultimo_registro < self._TIEMPO_MINIMO:
            return True  # Abuso detectado
            
        self._ultimas_consultas[user_id] = ahora
        return False

    def inicializar(self):
        """Configura la aplicación y conecta los controladores de presentación."""
        self.app = ApplicationBuilder().token(self.token).build()

        # Rutas del Controlador de Sistema
        self.app.add_handler(CommandHandler("start",      self.system_controller.cmd_start))
        self.app.add_handler(CommandHandler("reglamento", self.system_controller.cmd_reglamento))
        self.app.add_handler(CommandHandler("reset",      self.system_controller.cmd_reset))
        
        # Rutas del Controlador de Estadísticas de Carrera
        self.app.add_handler(CommandHandler("standings",    self.race_controller.cmd_standings))
        self.app.add_handler(CommandHandler("constructors", self.race_controller.cmd_constructors))
        self.app.add_handler(CommandHandler("lastrace",     self.race_controller.cmd_lastrace))
        self.app.add_handler(CommandHandler("nextrace",     self.race_controller.cmd_nextrace))
        
        # Rutas del Controlador del Quiz
        self.app.add_handler(CommandHandler("quiz",    self.quiz_controller.cmd_quiz))
        self.app.add_handler(CommandHandler("facil",   self.quiz_controller.cmd_facil))
        self.app.add_handler(CommandHandler("medio",   self.quiz_controller.cmd_medio))
        self.app.add_handler(CommandHandler("dificil", self.quiz_controller.cmd_dificil))
        
        # Manejo de Textos Libres y Notas de Voz
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.system_controller.manejar_mensaje))
        self.app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.system_controller.manejar_audio))

    def encender(self):
        """Lanza el bot en modo polling."""
        if not self.app:
            self.inicializar()
        logger.info("🏎️ Bot de Telegram iniciado y escuchando...")
        self.app.run_polling()
