from typing import Protocol, List, Optional
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult

class F1Gateway(Protocol):
    async def get_driver_standings(self) -> List[DriverStanding]:
        ...
    async def get_constructor_standings(self) -> List[ConstructorStanding]:
        ...
    async def get_last_race_results(self) -> Optional[RaceResult]:
        ...
