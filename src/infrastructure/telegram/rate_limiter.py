import time
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes
from src.infrastructure.settings.config import obtener_tiempo_minimo_consulta

class RateLimiter:
    def __init__(self):
        self._ultimas_consultas: Dict[int, float] = {}
        self._TIEMPO_MINIMO = obtener_tiempo_minimo_consulta()

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
            
        user_id = update.effective_user.id
        ahora = time.time()
        ultimo_registro = self._ultimas_consultas.get(user_id, 0)
        
        if ahora - ultimo_registro < self._TIEMPO_MINIMO:
            # Es spam, paramos la ejecución del handler
            raise Exception("Rate limit exceeded")
            
        self._ultimas_consultas[user_id] = ahora
