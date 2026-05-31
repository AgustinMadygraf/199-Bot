"""
Path: src/application/f1_use_case.py
"""

from typing import List, Optional
from src.application.ports.f1_gateway import F1Gateway
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult

class F1UseCase:
    def __init__(self, f1_gateway: F1Gateway):
        self._f1_gateway = f1_gateway

    async def get_driver_standings(self) -> List[DriverStanding]:
        return await self._f1_gateway.get_driver_standings()

    async def get_constructor_standings(self) -> List[ConstructorStanding]:
        return await self._f1_gateway.get_constructor_standings()

    async def get_last_race_results(self) -> Optional[RaceResult]:
        return await self._f1_gateway.get_last_race_results()
