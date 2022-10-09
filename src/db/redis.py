"""Интерфейс получения подключения к Redis."""

from aioredis import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    """Функция для внедрения зависимости от Redis.

    Returns:
        Асинхронный клиент для Redis.
    """
    return redis
