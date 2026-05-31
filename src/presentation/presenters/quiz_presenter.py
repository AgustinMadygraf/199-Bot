"""
Path: src/presentation/presenters/quiz_presenter.py
"""

from src.domain.entities.quiz import Pregunta

class QuizPresenter:
    def __init__(self):
        self.emojis = {"facil": "🟢", "medio": "🟡", "dificil": "🔴"}

    def formatear_menu_dificultad(self) -> str:
        return (
            "🏎️ ¡Bienvenido al Quiz de F1!\n\n"
            "Elegí la dificultad:\n"
            "🟢 /facil — Preguntas básicas\n"
            "🟡 /medio — Estrategia y reglamento\n"
            "🔴 /dificil — Datos técnicos avanzados"
        )

    def formatear_pregunta(self, dificultad: str, pregunta: Pregunta, texto_extra: str = "") -> str:
        emoji = self.emojis.get(dificultad, "❓")
        header = f"{emoji} Dificultad: {dificultad.upper()}\n5 preguntas. Respondé con A, B, C o D.\n\n"
        contenido = f"{pregunta.texto}\nOpciones: {', '.join(pregunta.opciones)}"
        
        if texto_extra:
            return f"{texto_extra}\n\n{header}{contenido}"
        return f"{header}{contenido}"

    def formatear_resultado(self, es_correcta: bool, respuesta_correcta: str, finalizado: bool, puntaje: int = 0, total: int = 0) -> str:
        resultado_txt = "✅ ¡Correcto!" if es_correcta else f"❌ Incorrecto. La respuesta era {respuesta_correcta}."
        
        if finalizado:
            return f"{resultado_txt}\n\nQuiz finalizado. Puntaje: {puntaje}/{total}."
        return resultado_txt
