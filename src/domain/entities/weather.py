"""
Path: src/domain/entities/weather.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class WeatherReport:
    temperature: float
    humidity: int
    description: str
