import pytest
from src.interface_adapters.presenters.f1_formatter import F1Formatter
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult

@pytest.fixture
def formatter():
    return F1Formatter()

def test_format_driver_standings_empty(formatter):
    assert formatter.format_driver_standings([]) == "No hay datos de clasificación de pilotos disponibles aún."

def test_format_driver_standings(formatter):
    standings = [
        DriverStanding(position=1, given_name="Lewis", family_name="Hamilton", constructor_name="Mercedes", points=25)
    ]
    result = formatter.format_driver_standings(standings)
    assert "🏆 CAMPEONATO DE PILOTOS" in result
    assert "P 1. Lewis Hamilton (Mercedes) — 25 pts" in result

def test_format_constructor_standings_empty(formatter):
    assert formatter.format_constructor_standings([]) == "No hay datos de clasificación de constructores disponibles aún."

def test_format_constructor_standings(formatter):
    standings = [
        ConstructorStanding(position=1, constructor_name="Mercedes", points=400)
    ]
    result = formatter.format_constructor_standings(standings)
    assert "🏗️ CAMPEONATO DE CONSTRUCTORES" in result
    assert "P 1. Mercedes — 400 pts" in result
