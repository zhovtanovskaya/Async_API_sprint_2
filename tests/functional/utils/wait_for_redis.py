import time

import redis
from redis.exceptions import ConnectionError

from tests.functional.settings import test_settings

if __name__ == '__main__':
    redis = redis.Redis(host=test_settings.redis_host, port=test_settings.redis_port, db=0)
    while True:
        try:
            if redis.ping():
                break
        except ConnectionError:
            time.sleep(1)
