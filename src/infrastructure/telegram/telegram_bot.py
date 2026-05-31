from typing import Any, Optional
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from src.infrastructure.settings.config import obtener_token_telegram
from src.infrastructure.settings.logger import logger
from src.infrastructure.telegram.rate_limiter import RateLimiter
from src.infrastructure.telegram.controller_registry import ControllerRegistry

class TelegramBot:
    """Encapsula la infraestructura específica de Telegram para aislar el main.py."""
    
    def __init__(self, registry: ControllerRegistry):
        self.token = obtener_token_telegram()
        self.registry = registry
        self.app: Optional[Any] = None
        self.rate_limiter = RateLimiter()

    def inicializar(self):
        """Configura la aplicación y conecta los controladores registrados con el middleware."""
        self.app = ApplicationBuilder().token(self.token).build()

        system_ctrl = self.registry.get("system")
        race_ctrl = self.registry.get("race")
        quiz_ctrl = self.registry.get("quiz")

        # Helper para añadir handlers con middleware
        def add_handler_with_limit(handler):
            original_callback = handler.callback
            async def wrapped_callback(update, context):
                try:
                    await self.rate_limiter(update, context)
                    await original_callback(update, context)
                except Exception:
                    logger.warning(f"Rate limit hit for user {update.effective_user.id}")
            handler.callback = wrapped_callback
            self.app.add_handler(handler)

        # Rutas registradas
        add_handler_with_limit(CommandHandler("start",      system_ctrl.cmd_start))
        add_handler_with_limit(CommandHandler("reglamento", system_ctrl.cmd_reglamento))
        add_handler_with_limit(CommandHandler("reset",      system_ctrl.cmd_reset))
        
        add_handler_with_limit(CommandHandler("standings",    race_ctrl.cmd_standings))
        add_handler_with_limit(CommandHandler("constructors", race_ctrl.cmd_constructors))
        add_handler_with_limit(CommandHandler("lastrace",     race_ctrl.cmd_lastrace))
        add_handler_with_limit(CommandHandler("nextrace",     race_ctrl.cmd_nextrace))
        
        add_handler_with_limit(CommandHandler("quiz",    quiz_ctrl.cmd_quiz))
        add_handler_with_limit(CommandHandler("facil",   quiz_ctrl.cmd_facil))
        add_handler_with_limit(CommandHandler("medio",   quiz_ctrl.cmd_medio))
        add_handler_with_limit(CommandHandler("dificil", quiz_ctrl.cmd_dificil))
        
        add_handler_with_limit(MessageHandler(filters.TEXT & ~filters.COMMAND, system_ctrl.manejar_mensaje))
        add_handler_with_limit(MessageHandler(filters.VOICE | filters.AUDIO, system_ctrl.manejar_audio))

    def encender(self):
        if not self.app:
            self.inicializar()
        logger.info("🏎️ Bot de Telegram iniciado y escuchando...")
        self.app.run_polling()
