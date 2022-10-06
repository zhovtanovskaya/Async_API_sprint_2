from http import HTTPStatus

import pytest

from tests.functional.settings import test_settings
from tests.functional.src.api_requests import make_get_request
from tests.functional.src.elastic import es_client, es_write_data
from tests.functional.src.redis_cache import redis_client, flush_cache


@pytest.fixture
def es_write_to_index(es_write_data):
    return lambda data: es_write_data(data, test_settings.elastic_index_mapping['genres'])


@pytest.fixture
def es_data():
    return [
        {
            'id': '5373d043-3f41-4ea8-9947-4b746c601bcc',
            "name": "Action",
            "description": None,
            "film_ids": [],
        },
    ]


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'id': '5373d043-3f41-4ea8-9947-4b746c601bcc'},
            {'status': HTTPStatus.OK},
            {'name': 'Action'},
        ),
        (
            {'id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
            {'status': HTTPStatus.NOT_FOUND},
            {'detail': 'Genre not found.'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request(f'/api/v1/genres/{request_data["id"]}')
    body = await response.json()
    assert response.status == response_data['status']
    assert body.items() >= response_body.items()


@pytest.mark.parametrize(
    'response_data',
    [
        (
            {'status': HTTPStatus.OK}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genres(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        response_data,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request('/api/v1/genres/')
    body = await response.json()
    assert response.status == response_data['status']
    assert len(body) > 0
