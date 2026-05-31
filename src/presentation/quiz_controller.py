from telegram import Update
from telegram.ext import ContextTypes
from src.application.quiz_use_case import QuizUseCase
from src.presentation.presenters.quiz_presenter import QuizPresenter

class QuizController:
    """Controlador que maneja la interacción de comandos de la Trivia con Telegram."""
    
    def __init__(self, quiz_use_case: QuizUseCase, presenter: QuizPresenter):
        self.quiz_use_case = quiz_use_case
        self.presenter = presenter

    async def cmd_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.presenter.formatear_menu_dificultad())

    async def iniciar_dificultad(self, update: Update, context: ContextTypes.DEFAULT_TYPE, dificultad: str):
        user_id = update.effective_user.id
        
        pregunta = self.quiz_use_case.iniciar_quiz(user_id, dificultad)
        if not pregunta:
            await update.message.reply_text("No hay preguntas disponibles.")
            return
        
        await update.message.reply_text(self.presenter.formatear_pregunta(dificultad, pregunta))

    async def responder(self, update: Update, context: ContextTypes.DEFAULT_TYPE, respuesta: str):
        user_id = update.effective_user.id
        try:
            es_correcta, pregunta_respondida, finalizado, puntaje, total = self.quiz_use_case.responder(user_id, respuesta)
            
            # Formatear el resultado
            texto_resultado = self.presenter.formatear_resultado(
                es_correcta, pregunta_respondida.respuesta_correcta, finalizado, puntaje, total
            )
            
            # Si no ha terminado, obtener la siguiente
            if not finalizado:
                # OJO: Necesitamos saber la dificultad para formatear correctamente la siguiente pregunta
                # El QuizSession actual no parece exponer la dificultad fácilmente tras ser creada.
                # Asumiremos que el presenter puede manejarlo o mejorar la entidad.
                # Por ahora, un enfoque sencillo:
                pregunta_siguiente = self.quiz_use_case.sesiones[user_id].obtener_pregunta_actual()
                dificultad = self.quiz_use_case.sesiones[user_id].dificultad
                texto_respuesta = self.presenter.formatear_pregunta(dificultad, pregunta_siguiente, texto_resultado)
            else:
                texto_respuesta = texto_resultado
                
            await update.message.reply_text(texto_respuesta)
            
        except ValueError as e:
            await update.message.reply_text(str(e))

    async def cmd_facil(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "facil")

    async def cmd_medio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "medio")

    async def cmd_dificil(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "dificil")
