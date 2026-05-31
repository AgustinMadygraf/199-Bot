from typing import List, Optional
from src.application.ports.f1_gateway import F1Gateway
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult
from src.infrastructure.httpx.app import get_async_http_client
from src.interface_adapters.gateways.api import get_json
from src.infrastructure.settings.config import obtener_http_timeout
from src.infrastructure.mappers.f1_mapper import F1Mapper

class F1ApiGateway(F1Gateway):
    def __init__(self) -> None:
        self._timeout = obtener_http_timeout()
        self._mapper = F1Mapper()

    async def get_driver_standings(self) -> List[DriverStanding]:
        data = await get_json(get_async_http_client, "current/driverStandings", self._timeout)
        if not data:
            return []
        return self._mapper.map_driver_standings(data)

    async def get_constructor_standings(self) -> List[ConstructorStanding]:
        data = await get_json(get_async_http_client, "current/constructorStandings", self._timeout)
        if not data:
            return []
        return self._mapper.map_constructor_standings(data)

    async def get_last_race_results(self) -> Optional[RaceResult]:
        data = await get_json(get_async_http_client, "current/last/results", self._timeout)
        if not data:
            return None
        return self._mapper.map_race_result(data)
