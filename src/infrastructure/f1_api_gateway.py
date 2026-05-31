"""
Path: src/infrastructure/f1_api_gateway.py
"""

from typing import List, Optional
from src.application.ports.f1_gateway import F1Gateway
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult
from src.infrastructure.httpx.app import get_async_http_client
from src.interface_adapters.gateways.api import get_json
from src.infrastructure.settings.config import obtener_http_timeout

class F1ApiGateway(F1Gateway):
    def __init__(self) -> None:
        self._timeout = obtener_http_timeout()

    async def get_driver_standings(self) -> List[DriverStanding]:
        data = await get_json(get_async_http_client, "current/driverStandings", self._timeout)
        if not data:
            return []

        standings = data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings:
            return []

        rows = standings[0]["DriverStandings"]
        result: List[DriverStanding] = []
        for r in rows:
            d = r["Driver"]
            c = r["Constructors"][0]["name"] if r["Constructors"] else "—"
            result.append(DriverStanding(
                position=int(r['position']),
                given_name=d['givenName'],
                family_name=d['familyName'],
                constructor_name=c,
                points=float(r['points'])
            ))
        return result

    async def get_constructor_standings(self) -> List[ConstructorStanding]:
        data = await get_json(get_async_http_client, "current/constructorStandings", self._timeout)
        if not data:
            return []

        standings = data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings:
            return []

        rows = standings[0]["ConstructorStandings"]
        return [
            ConstructorStanding(
                position=int(r['position']),
                constructor_name=r['Constructor']['name'],
                points=float(r['points'])
            ) for r in rows
        ]

    async def get_last_race_results(self) -> Optional[RaceResult]:
        data = await get_json(get_async_http_client, "current/last/results", self._timeout)
        if not data:
            return None

        races = data["MRData"]["RaceTable"]["Races"]
        if not races:
            return None

        race = races[0]
        return RaceResult(
            race_name=race['raceName'],
            circuit_name=race['Circuit']['circuitName'],
            date=race['date'],
            time=race.get('time', 'N/A')
        )
