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

        cmd_ctrl = self.registry.get("command")
        msg_ctrl = self.registry.get("message")
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
                    user_id = update.effective_user.id if update.effective_user else 0 if update.effective_user else "unknown"
                    logger.warning(f"Rate limit hit or error for user {user_id}")
            
            handler.callback = wrapped_callback
            if self.app:
                self.app.add_handler(handler)

        async def f1_handler_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, controller_method: Callable[[], Awaitable[str]]):
            if not update.message or not update.effective_chat: return
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            response = await controller_method()
            if update.message:
                await update.message.reply_text(response)

        # Command handlers
        async def cmd_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                await update.message.reply_text(cmd_ctrl.get_start_message())
        
        async def cmd_reglamento_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                await update.message.reply_text(cmd_ctrl.get_reglamento_message())
            
        async def cmd_reset_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                await update.message.reply_text(cmd_ctrl.reset_history(update.effective_user.id if update.effective_user else 0))

        # Message handlers
        async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not update.message or not update.message.text or not update.effective_chat: return
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            try:
                frags = await msg_ctrl.procesar_mensaje(update.effective_user.id if update.effective_user else 0, update.effective_user.username if update.effective_user else "unknown" or "", update.message.text)
                for frag in frags:
                    await update.message.reply_text(frag)
            except Exception as e:
                logger.error(f"Error: {e}")
                await update.message.reply_text("⚠️ Error técnico.")

        async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not update.message or not update.message.voice or not update.effective_chat: return
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")
            try:
                archivo_voz = await context.bot.get_file(update.message.voice.file_id)
                res = await msg_ctrl.procesar_audio(update.effective_user.id if update.effective_user else 0, update.effective_user.username if update.effective_user else "unknown" or "", archivo_voz.file_path)
                if not res:
                    await update.message.reply_text("No pude entender el audio.")
                else:
                    await update.message.reply_text(res, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Error: {e}")
                await update.message.reply_text("⚠️ Error procesando audio.")

        add_handler_with_limit(CommandHandler("start",      cmd_start_handler))
        add_handler_with_limit(CommandHandler("reglamento", cmd_reglamento_handler))
        add_handler_with_limit(CommandHandler("reset",      cmd_reset_handler))
        
        add_handler_with_limit(CommandHandler("standings",    lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_standings)))
        add_handler_with_limit(CommandHandler("constructors", lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_constructors)))
        add_handler_with_limit(CommandHandler("lastrace",     lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_lastrace)))
        add_handler_with_limit(CommandHandler("nextrace",     lambda u, c: f1_handler_wrapper(u, c, f1_ctrl.cmd_nextrace)))
        
        async def quiz_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                await update.message.reply_text(await quiz_ctrl.cmd_quiz())

        async def facil_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_facil(update.effective_user.id if update.effective_user else 0))

        async def medio_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_medio(update.effective_user.id if update.effective_user else 0))

        async def dificil_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.effective_user:
                await update.message.reply_text(await quiz_ctrl.cmd_dificil(update.effective_user.id if update.effective_user else 0))

        add_handler_with_limit(CommandHandler("quiz",    quiz_cmd_handler))
        add_handler_with_limit(CommandHandler("facil",   facil_cmd_handler))
        add_handler_with_limit(CommandHandler("medio",   medio_cmd_handler))
        add_handler_with_limit(CommandHandler("dificil", dificil_cmd_handler))
        
        add_handler_with_limit(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_handler))
        add_handler_with_limit(MessageHandler(filters.VOICE | filters.AUDIO, audio_handler))

    def encender(self):
        if not self.app:
            self.inicializar()
        if self.app:
            self.app.run_polling()
