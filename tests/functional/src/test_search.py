import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


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
                }
            ),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
def es_write_data():
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(
            data,
            test_settings.elastic_index,
            test_settings.elastic_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        es_client = AsyncElasticsearch(hosts=test_settings.elastic_host,
                                       validate_cert=False,
                                       use_ssl=False)
        response = await es_client.bulk(str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 100}
        ),
        (
                {'query': 'Mashedpotato'},
                {'status': 200, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, query_data, expected_answer):
    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
    } for _ in range(60)]
    await es_write_data(es_data)

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = test_settings.api_url + '/api/v1/films/search'
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
