"""
Path: src/infrastructure/telegram/telegram_bot.py
"""

from typing import Any, Optional, Callable, Awaitable
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    BaseHandler,
    Application
)
from src.infrastructure.settings.config import obtener_token_telegram
from src.infrastructure.settings.logger import logger
from src.infrastructure.telegram.rate_limiter import RateLimiter
from src.infrastructure.telegram.controller_registry import ControllerRegistry

class TelegramBot:

    def __init__(self, registry: ControllerRegistry):
        self.token = obtener_token_telegram()
        self.registry = registry
        self.app: Optional[Application[Any, Any, Any, Any, Any, Any]] = None
        self.rate_limiter = RateLimiter()

    def inicializar(self):
        self.app = ApplicationBuilder().token(self.token).build()

        system_ctrl = self.registry.get("system")
        f1_ctrl = self.registry.get("race")
        quiz_ctrl = self.registry.get("quiz")

        def add_handler_with_limit(handler: BaseHandler[Any, Any, Any]):
            original_callback = handler.callback
            async def wrapped_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
                try:
                    await self.rate_limiter(update, context)
                    await original_callback(update, context)
                except Exception as e:
                    logger.error(f"Error en wrapped_callback: {e}")
                    user_id = update.effective_user.id if update.effective_user else "unknown"
                    logger.warning(f"Rate limit hit or error for user {user_id}")
            
            handler.callback = wrapped_callback
            if self.app:
                self.app.add_handler(handler)

        async def f1_handler_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, controller_method: Callable[[], Awaitable[str]]):
            if not update.message or not update.effective_chat: return
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            response = await controller_method()
            await update.message.reply_text(response)

        add_handler_with_limit(CommandHandler("start",      system_ctrl.cmd_start))
        add_handler_with_limit(CommandHandler("reglamento", system_ctrl.cmd_reglamento))
        add_handler_with_limit(CommandHandler("reset",      system_ctrl.cmd_reset))
        
        add_handler_with_limit(CommandHandler("standings",    lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_standings)))
        add_handler_with_limit(CommandHandler("constructors", lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_constructors)))
        add_handler_with_limit(CommandHandler("lastrace",     lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_lastrace)))
        add_handler_with_limit(CommandHandler("nextrace",     lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_nextrace)))
        
        async def quiz_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                await update.message.reply_text(await quiz_ctrl.cmd_quiz())

        async def facil_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_facil(update.effective_user.id))

        async def medio_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_medio(update.effective_user.id))

        async def dificil_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_dificil(update.effective_user.id))

        add_handler_with_limit(CommandHandler("quiz",    quiz_cmd_handler))
        add_handler_with_limit(CommandHandler("facil",   facil_cmd_handler))
        add_handler_with_limit(CommandHandler("medio",   medio_cmd_handler))
        add_handler_with_limit(CommandHandler("dificil", dificil_cmd_handler))
        
        add_handler_with_limit(MessageHandler(filters.TEXT & ~filters.COMMAND, system_ctrl.manejar_mensaje))
        add_handler_with_limit(MessageHandler(filters.VOICE | filters.AUDIO, system_ctrl.manejar_audio))

    def encender(self):
        if not self.app:
            self.inicializar()
        if self.app:
            self.app.run_polling()
