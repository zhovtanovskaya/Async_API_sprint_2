"""Фикстуры для работы с кэшем в Redis."""

import aioredis
import pytest

from tests.functional.settings import test_settings


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
    )
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def flush_cache(redis_client):
    await redis_client.flushall()
