"""Настройки функциональных тестов."""

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """Настройки функциональных тестов."""

    elastic_host: str = '127.0.0.1'
    elastic_port: int = 9200
    elastic_id_field: str = 'id'
    elastic_index_mapping: dict = {
        'movies': 'movies',
        'genres': 'genres',
        'persons': 'persons',
    }
    redis_host: str = ''
    redis_port: int = 6379
    api_url: str = 'http://127.0.0.1:8000'


test_settings = TestSettings()
