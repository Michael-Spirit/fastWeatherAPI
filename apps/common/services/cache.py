from typing import Callable
from typing import Type

import aioredis
from fastapi_cache import Coder
from fastapi_cache import default_key_builder
from fastapi_cache import JsonCoder
from fastapi_cache.backends.redis import RedisBackend

from config.main import settings


class Cache:
    _backend = None
    _singleton_redis = None
    _redis = None
    _prefix = ''
    _coder: Type[Coder]

    @classmethod
    def set_redis(cls, redis):
        cls._singleton_redis = redis

    def __init__(
        self,
        prefix: str = settings.CACHE_KEY_PREFIX,
        coder: Type[Coder] = JsonCoder,
        key_builder: Callable = default_key_builder,
    ):
        self._prefix = prefix
        self._coder = coder
        self._key_builder = key_builder

        if Cache._singleton_redis:
            self._redis = Cache._singleton_redis

    async def __aenter__(self):
        if not self._redis:
            self._redis = aioredis.from_url(
                settings.REDIS_URL,
                encoding='utf8',
                decode_responses=True,
            )
        self._backend = RedisBackend(self._redis)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not Cache._singleton_redis and self._redis:
            await self._redis.close()
            await self._redis.connection_pool.disconnect()
            self._redis = None

    def get_prefix(self) -> str:
        return self._prefix

    def get_backend(self) -> RedisBackend:
        return self._backend

    def get_coder(self) -> Type[Coder]:
        return self._coder

    def get_key_builder(self) -> Callable:
        return self._key_builder

    async def clear(self, namespace: str = None, key: str = None):
        if self._backend:
            namespace = self._prefix + ':' + namespace if namespace else None
            return await self._backend.clear(namespace, key)
