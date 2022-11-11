import json
import logging
from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi_cache.backends.redis import RedisBackend
from pydantic import ValidationError

from apps.common.services.cache import Cache
from apps.weather.models.weather import WeatherData
from config.main import settings

logger = logging.getLogger(__name__)


class WeatherCache:
    CACHE_PREFIX = 'weather-cache'

    @classmethod
    async def store(cls, zipcode: str, weather_data: WeatherData):
        async with Cache() as cache:
            backend: RedisBackend = cache.get_backend()

            await backend.set(
                f'{cls.CACHE_PREFIX}/{zipcode}',
                json.dumps(jsonable_encoder(weather_data)),
                expire=settings.WEATHER_CACHE_EXPIRE_IN_SECONDS,
            )

    @classmethod
    async def get(cls, zipcode: str) -> Optional[WeatherData]:
        stored_data = await cls.fetch(zipcode)

        try:
            return WeatherData(**stored_data)
        except ValidationError:
            return None

    @classmethod
    async def fetch(cls, zipcode: str):
        async with Cache() as cache:
            backend: RedisBackend = cache.get_backend()
            payload = await backend.get(f'{cls.CACHE_PREFIX}/{zipcode}')

        if payload:
            return json.loads(payload)
        return {}
