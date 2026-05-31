"""
Path: src/application/tutor_use_case.py
"""

from typing import List
from src.domain.entities.chat_message import ChatMessage
from src.application.ports.tutor_ports import (
    LLMClient, 
    KnowledgeRepository, 
    HistoryRepository, 
    PromptRepository
)

class TutorUseCase:
    """Caso de uso que coordina la IA para responder como un profesor de F1,
    usando inyección de dependencias para delegar infraestructura y prompts.
    """
    
    def __init__(
        self, 
        llm_client: LLMClient, 
        knowledge_repo: KnowledgeRepository, 
        history_repo: HistoryRepository,
        prompt_repo: PromptRepository
    ):
        self.llm_client = llm_client
        self.knowledge_repo = knowledge_repo
        self.history_repo = history_repo
        self.prompt_repo = prompt_repo
        self.max_historial = 20

    async def ejecutar_consulta(self, user_id: int, mensaje_usuario: str) -> str:
        """Coordina todo el flujo de recopilación de datos, llamada al LLM y limpieza de respuesta."""
        
        datos_vivos = await self.knowledge_repo.obtener_datos_vivos(mensaje_usuario)
        datos_reglamento = self.knowledge_repo.buscar_reglamento(mensaje_usuario)

        extras = ""
        if datos_vivos:
            extras += f"\n\n[DATOS EN VIVO]\n{datos_vivos}\n[/DATOS EN VIVO]"
        if datos_reglamento:
            extras += f"\n\n{datos_reglamento}"

        mensaje_enriquecido = mensaje_usuario + extras
        
        mensajes = self._armar_contexto_contextual(user_id, mensaje_enriquecido)

        texto_respuesta = await self.llm_client.generar_respuesta(mensajes)

        self._guardar_asistente_en_historial(user_id, texto_respuesta)

        return self._limpiar_texto(texto_respuesta)

    def _armar_contexto_contextual(self, user_id: int, mensaje_enriquecido: str) -> List[ChatMessage]:
        historial = self.history_repo.cargar(user_id)
        historial.append(ChatMessage(role="user", content=mensaje_enriquecido))
        self.history_repo.guardar(user_id, historial)
        
        # Cargamos el prompt dinámicamente para reflejar cambios en conocimiento o personalidad
        system_prompt_template = self.prompt_repo.obtener_system_prompt()
        system_prompt = system_prompt_template.format(
            static_knowledge=self.knowledge_repo.static_knowledge
        )
        
        return [ChatMessage(role="system", content=system_prompt)] + historial[-self.max_historial:]

    def _guardar_asistente_en_historial(self, user_id: int, respuesta: str) -> None:
        historial = self.history_repo.cargar(user_id)
        historial.append(ChatMessage(role="assistant", content=respuesta))
        self.history_repo.guardar(user_id, historial)

    def _limpiar_texto(self, texto: str) -> str:
        frases_prohibidas = self.prompt_repo.obtener_frases_prohibidas()
        for frase in frases_prohibidas:
            texto = texto.replace(frase, "")
        texto = texto.replace("Sin embargo, ,", "Sin embargo,")
        return texto.strip()
