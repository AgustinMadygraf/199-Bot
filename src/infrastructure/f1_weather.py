"""
Path: src/infrastructure/f1_weather.py
"""

from src.infrastructure.httpx.app import get_http_client
from src.interface_adapters.gateways.api import get_openweather_report


def get_circuit_weather(lat: float, lon: float, api_key: str) -> str:
    """
    Obtiene el pronóstico del clima para las coordenadas de un circuito.
    Usa el plan gratuito de 5 días / 3 horas de OpenWeather.
    """
    return get_openweather_report(get_http_client, lat, lon, api_key)
