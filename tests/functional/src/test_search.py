import uuid
import json

import aiohttp
import aioredis
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
async def es_client():
    hosts = [f'{test_settings.elastic_host}:{test_settings.elastic_port}']
    client = AsyncElasticsearch(hosts=hosts)
    yield client
    await client.close()


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
    )
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(
            data,
            test_settings.elastic_index,
            test_settings.elastic_id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_delete_data(es_client):
    async def inner(data: list[dict]):
        for obj in data:
            await es_client.delete(test_settings.elastic_index, obj['id'])
    return inner


@pytest.fixture
def make_get_request():
    async def inner(path, query_data):
        session = aiohttp.ClientSession()
        url = test_settings.api_url + path
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return response
    return inner


@pytest.fixture
async def flush_cache(redis_client):
    await redis_client.flushall()


@pytest.fixture
def es_data():
    return [{
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


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star'},
            {'status': 200, 'length': 100},
        ),
        (
            {'query': 'Mashedpotato'},
            {'status': 200, 'length': 0},
        ),
        (
            {'query': 'The Star', 'page[size]': 0},
            {'status': 200, 'length': 0},
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(
        es_data,
        es_write_data,
        make_get_request,
        flush_cache,
        query_data,
        expected_answer,
        ):
    await es_write_data(es_data)
    # Запросить данные из ES по API.
    response = await make_get_request('/api/v1/films/search', query_data)
    body = await response.json()
    # Проверить ответ.
    assert response.status == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star'},
            {'status': 200, 'length': 100},
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_in_cache(
        es_data,
        es_write_data,
        es_delete_data,
        make_get_request,
        flush_cache,
        query_data,
        expected_answer,
        ):
    await es_write_data(es_data)
    # Сделать запрос, который закэширует фильм.
    await make_get_request('/api/v1/films/search', query_data)
    # Удалить фильм из ES.
    await es_delete_data(es_data)
    # Запросить данные из ES по API.
    response = await make_get_request('/api/v1/films/search', query_data)
    body = await response.json()
    # Проверить ответ.
    assert response.status == expected_answer['status']
    assert len(body) == expected_answer['length']
