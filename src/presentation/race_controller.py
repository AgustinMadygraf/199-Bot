from telegram import Update
from telegram.ext import ContextTypes
from src.application.ports.f1_gateway import F1Gateway
from src.domain.services.time_utils import convert_utc_to_local

class RaceController:
    """Controlador encargado de despachar la información y estadísticas en vivo de la F1."""
    
    def __init__(self, f1_gateway: F1Gateway):
        self._f1_gateway = f1_gateway

    async def cmd_standings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.effective_chat: return
        chat_id = update.effective_chat.id
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        standings = await self._f1_gateway.get_driver_standings()
        
        if not standings:
            await update.message.reply_text("No hay datos de clasificación disponibles aún.")
            return

        lines = [f"🏆 CAMPEONATO DE PILOTOS\n"]
        for r in standings:
            lines.append(
                f"P{r.position:>2}. {r.given_name} {r.family_name} ({r.constructor_name}) "
                f"— {r.points} pts"
            )
        await update.message.reply_text("\n".join(lines))

    async def cmd_constructors(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.effective_chat: return
        chat_id = update.effective_chat.id
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        standings = await self._f1_gateway.get_constructor_standings()
        
        if not standings:
            await update.message.reply_text("No hay datos de clasificación disponibles aún.")
            return

        lines = [f"🏗️ CAMPEONATO DE CONSTRUCTORES\n"]
        for r in standings:
            lines.append(f"P{r.position:>2}. {r.constructor_name} — {r.points} pts")
        await update.message.reply_text("\n".join(lines))

    async def cmd_lastrace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.effective_chat: return
        chat_id = update.effective_chat.id
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        result = await self._f1_gateway.get_last_race_results()
        
        if not result:
            await update.message.reply_text("No hay resultados de la última carrera disponibles.")
            return

        formatted_date = convert_utc_to_local(result.date, result.time)
        response = (
            f"🏁 {result.race_name.upper()} — {result.circuit_name}\n"
            f"📅 {formatted_date}"
        )
        await update.message.reply_text(response)

    async def cmd_nextrace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.effective_chat: return
        chat_id = update.effective_chat.id
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        # Nota: La funcionalidad cmd_nextrace requiere implementar F1Gateway.get_next_race
        await update.message.reply_text("Funcionalidad de próxima carrera aún no implementada en el Gateway.")
