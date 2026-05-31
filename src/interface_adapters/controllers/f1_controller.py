"""
Path: src/interface_adapters/controllers/f1_controller.py
"""

from src.application.f1_use_case import F1UseCase
from src.interface_adapters.presenters.f1_formatter import F1Formatter

class F1Controller:
    def __init__(self, f1_use_case: F1UseCase, formatter: F1Formatter):
        self.f1_use_case = f1_use_case
        self.formatter = formatter

    async def cmd_standings(self) -> str:
        standings = await self.f1_use_case.get_driver_standings()
        return self.formatter.format_driver_standings(standings)

    async def cmd_constructors(self) -> str:
        standings = await self.f1_use_case.get_constructor_standings()
        return self.formatter.format_constructor_standings(standings)

    async def cmd_lastrace(self) -> str:
        result = await self.f1_use_case.get_last_race_results()
        return self.formatter.format_last_race_results(result)

    async def cmd_nextrace(self) -> str:
        return "Funcionalidad de próxima carrera aún no implementada."
