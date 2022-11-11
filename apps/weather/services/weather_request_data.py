import logging

from httpx import AsyncClient
from pyowm import OWM

from apps.weather.models.weather import ObservationResponse
from apps.weather.models.weather import WeatherData
from apps.weather.services.weather_cache import WeatherCache
from config.main import settings

logger = logging.getLogger(__name__)


class RequestWeatherDataClient(AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weather_manager = OWM(settings.OPEN_WEATHER_MAP_API_KEY).weather_manager()

    async def search_weather_for_zipcode(self, zipcode: str) -> WeatherData:
        observation = await self._request_observation(zipcode)

        formatted_weather_data = observation.to_weather_data()
        await WeatherCache.store(zipcode, formatted_weather_data)  # cache after 3rd party request

        return formatted_weather_data

    async def _request_observation(self, zipcode: str) -> ObservationResponse:
        response = self.weather_manager.weather_at_zip_code(zipcode, 'us')
        return ObservationResponse(**response.to_dict())
