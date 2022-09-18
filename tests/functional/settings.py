from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_index: str = 'movies'
    es_id_field: str = 'id'
    es_index_mapping: dict = ''

    redis_host: str = ''
    service_url: str = 'http://127.0.0.1:8500'


test_settings = TestSettings()