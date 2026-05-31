import pytest
from unittest.mock import MagicMock
from src.interface_adapters.controllers.quiz_controller import QuizController
from src.application.quiz_use_case import QuizUseCase
from src.interface_adapters.presenters.quiz_formatter import QuizFormatter
from src.domain.entities.quiz import Pregunta

@pytest.mark.asyncio
async def test_cmd_quiz_returns_formatted_menu():
    # Arrange
    use_case = MagicMock(spec=QuizUseCase)
    presenter = MagicMock(spec=QuizFormatter)
    presenter.formatear_menu_dificultad.return_value = "Menu"
    controller = QuizController(use_case, presenter)
    
    # Act
    result = await controller.cmd_quiz()
    
    # Assert
    assert result == "Menu"
    presenter.formatear_menu_dificultad.assert_called_once()

@pytest.mark.asyncio
async def test_iniciar_dificultad_returns_formatted_pregunta():
    # Arrange
    use_case = MagicMock(spec=QuizUseCase)
    pregunta = MagicMock(spec=Pregunta)
    use_case.iniciar_quiz.return_value = pregunta
    
    presenter = MagicMock(spec=QuizFormatter)
    presenter.formatear_pregunta.return_value = "Pregunta Formateada"
    
    controller = QuizController(use_case, presenter)
    
    # Act
    result = await controller.iniciar_dificultad(123, "facil")
    
    # Assert
    assert result == "Pregunta Formateada"
    use_case.iniciar_quiz.assert_called_once_with(123, "facil")
    presenter.formatear_pregunta.assert_called_once_with("facil", pregunta)

@pytest.mark.asyncio
async def test_responder_returns_formatted_result():
    # Arrange
    use_case = MagicMock(spec=QuizUseCase)
    pregunta = MagicMock(spec=Pregunta)
    pregunta.respuesta_correcta = "A"
    # mock responder return: es_correcta, pregunta_respondida, finalizado, puntaje, total
    use_case.responder.return_value = (True, pregunta, True, 5, 5)
    
    presenter = MagicMock(spec=QuizFormatter)
    presenter.formatear_resultado.return_value = "Resultado Final"
    
    controller = QuizController(use_case, presenter)
    
    # Act
    result = await controller.responder(123, "A")
    
    # Assert
    assert result == "Resultado Final"
    use_case.responder.assert_called_once_with(123, "A")
    presenter.formatear_resultado.assert_called_once_with(True, "A", True, 5, 5)
