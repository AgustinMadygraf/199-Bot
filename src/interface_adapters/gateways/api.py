"""
Path: src/interface_adapters/gateways/api.py
"""

from collections.abc import Callable
from typing import Any

BASE_URL = "https://api.jolpi.ca/ergast/f1"

AsyncClientFactory = Callable[[float], Any]
SyncClientFactory = Callable[[float], Any]


async def get_json(async_client_factory: AsyncClientFactory, endpoint: str, timeout: float) -> dict[str, Any] | None:
    """Obtiene JSON del endpoint de Jolpica/F1 y retorna None en caso de error."""
    try:
        async with async_client_factory(timeout) as client:
            response = await client.get(f"{BASE_URL}/{endpoint}.json")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"[F1 API] Error en {endpoint}: {e}")
        return None


def get_openweather_forecast(http_client_factory: SyncClientFactory, lat: float, lon: float, api_key: str, timeout: float) -> dict[str, Any] | None:
    """Solicita el pronóstico de OpenWeather y retorna el JSON o None."""
    if not api_key:
        return None

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
    )

    try:
        with http_client_factory(timeout) as client:
            response = client.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
    except Exception:
        return None


def format_openweather_report(data: dict[str, Any]) -> str:
    """Formatea el JSON de OpenWeather en una respuesta legible."""
    try:
        clima_actual = data["list"][0]
        temp = clima_actual["main"]["temp"]
        humedad = clima_actual["main"]["humidity"]
        descripcion = clima_actual["weather"][0]["description"].capitalize()
        return f"🌡️ {temp}°C | 💧 Humedad: {humedad}% | 🌤️ {descripcion}"
    except Exception:
        return "❌ No se pudo obtener el clima del circuito en este momento."


def get_openweather_report(http_client_factory: SyncClientFactory, lat: float, lon: float, api_key: str, timeout: float) -> str:
    """Retorna el reporte de clima usando OpenWeather."""
    if not api_key:
        return "⚠️ Error: OPENWEATHER_API_KEY no configurada en el entorno."

    data = get_openweather_forecast(http_client_factory, lat, lon, api_key, timeout)
    if data is None:
        return "❌ No se pudo obtener el clima del circuito en este momento."

    return format_openweather_report(data)
