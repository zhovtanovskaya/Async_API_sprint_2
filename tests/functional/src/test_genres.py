import uuid

import pytest

from tests.functional.src.elastic import es_client, es_write_data
from tests.functional.src.api_requests import make_get_request


@pytest.fixture
def es_write_to_index(es_write_data):
    return lambda data: es_write_data(data, 'genres')


@pytest.fixture
def es_data():
    return [
        {
            'id': '5373d043-3f41-4ea8-9947-4b746c601bcc',
            "name": "Action",
            "description": None,
            "film_ids": [],
        }
    ]


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'id': '5373d043-3f41-4ea8-9947-4b746c601bcc'},
            {'status': 200},
            {'name': 'Action'},
        ),
        (
            {'id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
            {'status': 404},
            {'detail': 'Genre not found.'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(
        es_data,
        es_write_to_index,
        make_get_request,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request(f'/api/v1/genres/{request_data["id"]}')
    body = await response.json()
    assert response.status == response_data['status']
    for key in response_body.keys():
        assert key in body
        assert body[key] == response_body[key]
