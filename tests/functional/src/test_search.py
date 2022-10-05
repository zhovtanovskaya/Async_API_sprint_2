import uuid
from http import HTTPStatus

import pytest

from tests.functional.settings import test_settings
from tests.functional.src.api_requests import make_get_request
from tests.functional.src.elastic import es_client, es_delete_data, es_write_data
from tests.functional.src.redis_cache import redis_client, flush_cache


@pytest.fixture
def es_write_to_index(es_write_data):
    return lambda data: es_write_data(data, test_settings.elastic_index)


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
            {'status': HTTPStatus.OK, 'length': 100},
        ),
        (
            {'query': 'Mashedpotato'},
            {'status': HTTPStatus.OK, 'length': 0},
        ),
        (
            {'query': 'The Star', 'page[size]': 0},
            {'status': HTTPStatus.OK, 'length': 0},
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        query_data,
        expected_answer,
        ):
    await es_write_to_index(es_data)
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
            {'status': HTTPStatus.OK, 'length': 100},
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_in_cache(
        es_data,
        es_write_to_index,
        es_delete_data,
        make_get_request,
        flush_cache,
        query_data,
        expected_answer,
        ):
    await es_write_to_index(es_data)
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
