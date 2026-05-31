from telegram import Update
from telegram.ext import ContextTypes
import uuid
from src.infrastructure.settings.logger import logger
from src.application.audio_use_case import AudioUseCase
from src.application.ports.tutor_ports import HistoryRepository

class SystemController:
    """Controlador que maneja comandos globales, interacciones de texto y mensajería de voz."""
    
    def __init__(self, audio_use_case: AudioUseCase, telegram_bot, chat_processor, rag_service, history_repository: HistoryRepository, quiz_controller=None):
        self.audio_use_case = audio_use_case
        self.telegram_bot = telegram_bot
        self.chat_processor = chat_processor
        self.rag_service = rag_service
        self.history_repository = history_repository
        self.quiz_controller = quiz_controller

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        rag_status = "✅ Reglamento FIA indexado" if self.rag_service and self.rag_service.reglamento_disponible() else "⏳ Reglamento no disponible"
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
        if self.rag_service and self.rag_service.reglamento_disponible():
            await update.message.reply_text(
                "✅ El reglamento oficial FIA 2026 está indexado y disponible.\n"
                "Preguntame cualquier duda sobre las reglas y busco directamente en el documento oficial."
            )
        else:
            await update.message.reply_text(
                "⏳ El reglamento todavía se está indexando o no está disponible. Intentá de nuevo en unos minutos."
            )

    async def cmd_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.history_repository.borrar(update.effective_user.id)
        await update.message.reply_text("✅ Historial borrado. ¡Volvemos a la largada!")

    async def manejar_mensaje(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        texto = update.message.text
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Si el usuario está en un quiz, derivamos la respuesta al QuizController
            if self.quiz_controller and self.quiz_controller.quiz_use_case.esta_jugando(user_id):
                respuesta = await self.quiz_controller.responder(user_id, texto)
            else:
                respuesta = await self.chat_processor.procesar(user_id, username, texto, "consulta_general")
            
            for i in range(0, len(respuesta), 4096):
                await update.message.reply_text(respuesta[i:i + 4096])
                
        except Exception as e:
            logger.error(f"Error en manejar_mensaje: {e}")
            await update.message.reply_text("⚠️ Error técnico. Intentá de nuevo.")

    async def manejar_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")
        
        try:
            archivo_voz = await context.bot.get_file(update.message.voice.file_id)
            texto_transcrito = await self.audio_use_case.transcribir(archivo_voz.file_path)
            
            if not texto_transcrito:
                await update.message.reply_text("No pude entender el audio. ¿Podés repetir?")
                return

            # Procesar el texto transcrito (igual que un mensaje de texto)
            if self.quiz_controller and self.quiz_controller.quiz_use_case.esta_jugando(user_id):
                respuesta = await self.quiz_controller.responder(user_id, texto_transcrito)
            else:
                respuesta = await self.chat_processor.procesar(user_id, username, texto_transcrito, "consulta_voz")

            await update.message.reply_text(f"🎤 *Entendido:* _{texto_transcrito}_\n\n{respuesta}", parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error en manejar_audio: {e}")
            await update.message.reply_text("⚠️ Error al procesar el audio.")
