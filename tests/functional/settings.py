from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    elastic_host: str = '127.0.0.1'
    elastic_index: str = 'movies'
    elastic_id_field: str = 'id'
    elastic_index_mapping: dict = ''
    redis_host: str = ''
    api_url: str = 'http://127.0.0.1:8000'


test_settings = TestSettings()