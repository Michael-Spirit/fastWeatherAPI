import asyncio

import pytest

from apps.common.services.cache import Cache
from apps.common.services.testing_client import TestClient


@pytest.fixture(scope='session')
def event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        return loop


@pytest.fixture(scope='session')
def app():
    from apps.app import app as api_app

    return api_app


@pytest.fixture(scope='session')
def client(app):
    return TestClient(app)


@pytest.fixture(autouse=True, scope='function')
async def setup_redis():
    yield

    async with Cache() as cache:
        await cache.flush()
