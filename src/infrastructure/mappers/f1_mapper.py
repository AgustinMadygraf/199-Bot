from typing import List, Optional, Dict, Any
from src.domain.entities.f1_models import DriverStanding, ConstructorStanding, RaceResult

class F1Mapper:
    @staticmethod
    def map_driver_standings(data: Dict[str, Any]) -> List[DriverStanding]:
        standings = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings:
            return []

        rows = standings[0].get("DriverStandings", [])
        result: List[DriverStanding] = []
        for r in rows:
            d = r["Driver"]
            c = r["Constructors"][0]["name"] if r.get("Constructors") else "—"
            result.append(DriverStanding(
                position=int(r['position']),
                given_name=d['givenName'],
                family_name=d['familyName'],
                constructor_name=c,
                points=float(r['points'])
            ))
        return result

    @staticmethod
    def map_constructor_standings(data: Dict[str, Any]) -> List[ConstructorStanding]:
        standings = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings:
            return []

        rows = standings[0].get("ConstructorStandings", [])
        return [
            ConstructorStanding(
                position=int(r['position']),
                constructor_name=r['Constructor']['name'],
                points=float(r['points'])
            ) for r in rows
        ]

    @staticmethod
    def map_race_result(data: Dict[str, Any]) -> Optional[RaceResult]:
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not races:
            return None

        race = races[0]
        return RaceResult(
            race_name=race['raceName'],
            circuit_name=race['Circuit']['circuitName'],
            date=race['date'],
            time=race.get('time', 'N/A')
        )
