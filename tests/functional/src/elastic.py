"""Фикстуры для работы с Elastic в тестах."""

import json

import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@pytest.fixture
async def es_client():
    hosts = [f'{test_settings.elastic_host}:{test_settings.elastic_port}']
    client = AsyncElasticsearch(hosts=hosts)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict], index, id_field='id'):
        bulk_query = get_es_bulk_query(data, index, id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_delete_data(es_client):
    async def inner(data: list[dict], index: str):
        for obj in data:
            await es_client.delete(index, obj['id'])
    return inner


def get_es_bulk_query(data, elastic_index, elastic_id_field):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps(
                {
                    'index': {
                        '_index': elastic_index,
                        '_id': row[elastic_id_field],
                    },
                },
            ),
            json.dumps(row)
        ])
    return bulk_query
