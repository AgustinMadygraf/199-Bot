"""
Path: tests/test_tutor_use_case.py
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.tutor_use_case import TutorUseCase

@pytest.mark.asyncio
async def test_tutor_use_case_loads_prompt_dynamically():
    # Mocks
    llm_client = AsyncMock()
    llm_client.generar_respuesta.return_value = "Respuesta de prueba"
    
    knowledge_repo = MagicMock()
    knowledge_repo.static_knowledge = "Conocimiento estático"
    knowledge_repo.obtener_datos_vivos = AsyncMock(return_value="")
    knowledge_repo.buscar_reglamento = MagicMock(return_value="")
    
    history_repo = MagicMock()
    history_repo.cargar.return_value = []
    
    prompt_repo = MagicMock()
    prompt_repo.obtener_system_prompt.return_value = "Prompt con {static_knowledge}"
    prompt_repo.obtener_frases_prohibidas.return_value = ["prohibido"]
    
    use_case = TutorUseCase(llm_client, knowledge_repo, history_repo, prompt_repo)
    
    # Ejecución
    respuesta = await use_case.ejecutar_consulta(1, "Hola")
    
    # Verificaciones
    assert respuesta == "Respuesta de prueba"
    prompt_repo.obtener_system_prompt.assert_called_once()
    llm_client.generar_respuesta.assert_called_once()
    
    # Verificar que el prompt se formateó correctamente
    args, _ = llm_client.generar_respuesta.call_args
    mensajes = args[0]
    assert mensajes[0].role == "system"
    assert "Conocimiento estático" in mensajes[0].content

@pytest.mark.asyncio
async def test_tutor_use_case_cleans_forbidden_phrases():
    llm_client = AsyncMock()
    llm_client.generar_respuesta.return_value = "Esta es una frase prohibida y secreta"
    
    knowledge_repo = MagicMock()
    knowledge_repo.static_knowledge = ""
    knowledge_repo.obtener_datos_vivos = AsyncMock(return_value="")
    knowledge_repo.buscar_reglamento = MagicMock(return_value="")
    
    history_repo = MagicMock()
    history_repo.cargar.return_value = []
    
    prompt_repo = MagicMock()
    prompt_repo.obtener_system_prompt.return_value = "Prompt"
    prompt_repo.obtener_frases_prohibidas.return_value = ["frase prohibida"]
    
    use_case = TutorUseCase(llm_client, knowledge_repo, history_repo, prompt_repo)
    
    respuesta = await use_case.ejecutar_consulta(1, "Hola")
    
    assert "frase prohibida" not in respuesta
    assert respuesta == "Esta es una  y secreta"
