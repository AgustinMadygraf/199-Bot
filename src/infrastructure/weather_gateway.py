from src.application.ports.weather_gateway import WeatherGateway
from src.interface_adapters.gateways.api import get_openweather_report
from src.infrastructure.httpx.app import get_http_client
from src.infrastructure.settings.config import obtener_openweather_api_key, obtener_http_timeout

class OpenWeatherGateway(WeatherGateway):
    def __init__(self):
        self.api_key = obtener_openweather_api_key()
        self.timeout = obtener_http_timeout()

    def get_weather_report(self, lat: float, lon: float) -> str:
        return get_openweather_report(get_http_client, lat, lon, self.api_key, self.timeout)
