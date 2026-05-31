"""
Path: src/application/ports/weather_gateway.py
"""

from typing import Protocol

class WeatherGateway(Protocol):
    def get_weather_report(self, lat: float, lon: float) -> str:
        ...
