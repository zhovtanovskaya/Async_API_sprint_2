"""Тесты REST API фильмов."""

from http import HTTPStatus

import pytest

from tests.functional.settings import test_settings
from tests.functional.src.api_requests import make_get_request
from tests.functional.src.elastic import (es_client, es_delete_data,
                                          es_write_data)
from tests.functional.src.redis_cache import flush_cache, redis_client


@pytest.fixture
def es_write_to_index(es_write_data):
    return lambda data: es_write_data(
        data, test_settings.elastic_index_mapping['movies'])


@pytest.fixture
def es_data():
    return [{
        'id': '4c730b51-539c-405d-b7c1-e25b70f11202',
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
    }]


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'id': '4c730b51-539c-405d-b7c1-e25b70f11202'},
            {'status': HTTPStatus.OK},
            {'title': 'The Star'},
        ),
        (
            {'id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
            {'status': HTTPStatus.NOT_FOUND},
            {'detail': 'film not found'},
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_id(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request(f'/api/v1/films/{request_data["id"]}')
    body = await response.json()
    assert response.status == response_data['status']
    assert body.items() >= response_body.items()


@pytest.mark.parametrize(
    'query_data, response_data',
    [
        (
            {},
            {'status': HTTPStatus.OK},
        ),
        (
                {'page[number]': 1, 'page[size]': 1},
                {'status': HTTPStatus.OK},
        ),
        (
                {'sort': '-imdb_rating'},
                {'status': HTTPStatus.OK},
        ),
        (
                {'genre': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
                {'status': HTTPStatus.OK},
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_films(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        query_data,
        response_data,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request('/api/v1/films', query_data)
    body = await response.json()
    assert response.status == response_data['status']
    assert len(body) > 0


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
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
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
    await es_delete_data(
        es_data, test_settings.elastic_index_mapping['movies'])
    # Запросить данные из ES по API.
    response = await make_get_request('/api/v1/films/search', query_data)
    body = await response.json()
    # Проверить ответ.
    assert response.status == expected_answer['status']
    assert len(body) == expected_answer['length']
