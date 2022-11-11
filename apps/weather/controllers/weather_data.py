import logging

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pyowm.commons.exceptions import NotFoundError

from apps.weather.router import router
from apps.weather.services.weather_cache import WeatherCache
from apps.weather.services.weather_request_data import RequestWeatherDataClient

logger = logging.getLogger(__name__)


@router.get('/api/weather/{zipcode}')
async def get_weather_by_zipcode(zipcode: str, force_update: bool = False):
    cached_weather = await WeatherCache.get(zipcode)

    if cached_weather and not force_update:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(cached_weather))

    weather_client = RequestWeatherDataClient()

    try:
        request_weather = await weather_client.search_weather_for_zipcode(zipcode)
    except NotFoundError as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(str(err)))

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(request_weather))
