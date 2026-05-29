"""
Path: src/presentation/system_controller.py
"""

import os
import uuid
from telegram import Update
from telegram.ext import ContextTypes

from src.infrastructure.settings.logger import logger
from src.infrastructure.f1_rag import reglamento_disponible

class SystemController:
    """Controlador que maneja comandos globales, interacciones de texto y mensajería de voz con seguridad avanzada."""
    
    def __init__(self, audio_service, telegram_bot, chat_processor):
        self.audio_service = audio_service
        self.telegram_bot = telegram_bot
        self.chat_processor = chat_processor

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        rag_status = "✅ Reglamento FIA indexado" if reglamento_disponible() else "⏳ Indexando reglamento..."
        await update.message.reply_text(
            "🏎️ ¡Bienvenido al Bot educativo de F1!\n\n"
            "Podés preguntarme lo que quieras sobre Fórmula 1:\n"
            "• Reglamento técnico y deportivo\n"
            "• Pilotos y escuderías\n"
            "• Circuitos y estrategias\n"
            "• Clasificaciones y resultados en vivo\n\n"
            f"Estado: {rag_status}\n\n"
            "Comandos disponibles:\n"
            "/standings — Clasificación de pilotos\n"
            "/constructors — Clasificación de constructores\n"
            "/lastrace — Resultado de la última carrera\n"
            "/nextrace — Próxima carrera\n"
            "/reglamento — Estado del reglamento indexado\n"
            "/quiz — Poné a prueba tus conocimientos de F1\n"
            "/reset — Borrar historial de conversación\n\n"
            "¿Por dónde empezamos? 🏁"
        )

    async def cmd_reglamento(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if reglamento_disponible():
            await update.message.reply_text(
                "✅ El reglamento oficial FIA 2026 está indexado y disponible.\n"
                "Preguntame cualquier duda sobre las reglas y busco directamente en el documento oficial."
            )
        else:
            await update.message.reply_text(
                "⏳ El reglamento todavía se está indexando. Intentá de nuevo en unos minutos."
            )

    async def cmd_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from src.infrastructure.db import borrar_historial
        borrar_historial(update.effective_user.id)
        await update.message.reply_text("✅ Historial borrado. ¡Volvemos a la largada!")

    async def manejar_mensaje(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        texto = update.message.text
        
        if self.telegram_bot.es_spammer(user_id):
            await update.message.reply_text("⚠️ ¡Boxes llenos! Por favor, esperá unos segundos antes de enviar otro mensaje.")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            respuesta = await self.chat_processor.procesar(user_id, username, texto, "consulta_general")
            
            for i in range(0, len(respuesta), 4096):
                await update.message.reply_text(respuesta[i:i + 4096])
                
        except Exception as e:
            logger.error(f"Error en manejar_mensaje: {e}")
            await update.message.reply_text("⚠️ Error técnico. Intentá de nuevo.")

    async def manejar_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        if self.telegram_bot.es_spammer(user_id):
            await update.message.reply_text("⚠️ ¡Boxes llenos! Esperá unos segundos antes de mandar otro audio.")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        path = None
        try:
            voice = update.message.voice or update.message.audio
            file = await context.bot.get_file(voice.file_id)
            
            id_unico = uuid.uuid4().hex[:6]
            path = f"audio_{user_id}_{id_unico}.ogg"
            
            await file.download_to_drive(path)
            
            texto = await self.audio_service.transcribir_ogg(path)
            
            if os.path.exists(path):
                os.remove(path)
                path = None
                
            await update.message.reply_text(f"🎙️ Escuché: _{texto}_", parse_mode="Markdown")
            
            respuesta = await self.chat_processor.procesar(user_id, username, texto, "consulta_general_audio")
            
            for i in range(0, len(respuesta), 4096):
                await update.message.reply_text(respuesta[i:i + 4096])
                
        except Exception as e:
            logger.error(f"Error en audio: {e}")
            await update.message.reply_text("⚠️ No pude procesar el audio.")
            
        finally:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logger.error(f"No se pudo limpiar el archivo residual {path}: {e}")
