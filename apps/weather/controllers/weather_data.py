import logging

from fastapi import HTTPException
from fastapi import status
from pyowm.commons.exceptions import NotFoundError

from apps.weather.models.weather import WeatherData
from apps.weather.router import router
from apps.weather.services.weather_cache import WeatherCache
from apps.weather.services.weather_request_data import RequestWeatherDataClient

logger = logging.getLogger(__name__)


@router.get('/api/weather/{zipcode}', response_model=WeatherData)
async def get_weather_by_zipcode(zipcode: str, force_update: bool = False):
    cached_weather = await WeatherCache.get(zipcode) if not force_update else None

    if not cached_weather:
        weather_client = RequestWeatherDataClient()

        try:
            cached_weather = await weather_client.search_weather_for_zipcode(zipcode)
        except NotFoundError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    return cached_weather
