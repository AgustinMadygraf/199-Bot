"""
Path: src/domain/entities/f1_models.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class DriverStanding:
    position: int
    given_name: str
    family_name: str
    constructor_name: str
    points: float

@dataclass(frozen=True)
class ConstructorStanding:
    position: int
    constructor_name: str
    points: float

@dataclass(frozen=True)
class RaceResult:
    race_name: str
    circuit_name: str
    date: str
    time: str
