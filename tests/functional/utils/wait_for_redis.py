"""Модуль для Docker, который дожидается старта Redis."""

import redis
from redis.exceptions import ConnectionError

from tests.functional.settings import test_settings
from tests.functional.utils.backoff import backoff


@backoff(exceptions=(ConnectionError,))
def ping_redis(host:str, port: int):
    client = redis.Redis(host=host, port=port, db=0)
    client.ping()


if __name__ == '__main__':
    ping_redis(test_settings.redis_host, test_settings.redis_port)
