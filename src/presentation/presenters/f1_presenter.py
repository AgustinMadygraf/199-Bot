"""
Path: src/presentation/presenters/f1_presenter.py
"""

from typing import List, Optional
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult
from src.domain.services.time_utils import convert_utc_to_local

class F1Presenter:
    def format_driver_standings(self, standings: List[DriverStanding]) -> str:
        if not standings:
            return "No hay datos de clasificación de pilotos disponibles aún."
        
        lines = ["🏆 CAMPEONATO DE PILOTOS\n"]
        for r in standings:
            lines.append(
                f"P{r.position:>2}. {r.given_name} {r.family_name} ({r.constructor_name}) "
                f"— {r.points} pts"
            )
        return "\n".join(lines)

    def format_constructor_standings(self, standings: List[ConstructorStanding]) -> str:
        if not standings:
            return "No hay datos de clasificación de constructores disponibles aún."
        
        lines = ["🏗️ CAMPEONATO DE CONSTRUCTORES\n"]
        for r in standings:
            lines.append(f"P{r.position:>2}. {r.constructor_name} — {r.points} pts")
        return "\n".join(lines)

    def format_last_race_results(self, result: Optional[RaceResult]) -> str:
        if not result:
            return "No hay resultados de la última carrera disponibles."

        formatted_date = convert_utc_to_local(result.date, result.time)
        return (
            f"🏁 {result.race_name.upper()} — {result.circuit_name}\n"
            f"📅 {formatted_date}"
        )
