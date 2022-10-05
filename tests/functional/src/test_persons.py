from http import HTTPStatus

import pytest

from tests.functional.src.api_requests import make_get_request
from tests.functional.src.elastic import es_client, es_write_data
from tests.functional.src.redis_cache import redis_client, flush_cache


@pytest.fixture
def es_write_to_index(es_write_data):
    return lambda data: es_write_data(data, 'persons')


@pytest.fixture
def es_data():
    return [
        {
            'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358',
            'name': 'Carrie Fisher',
            'film_ids': [
                '025c58cd-1b7e-43be-9ffb-8571a613579b',
             ],
            'role': ['actor'],
        },
    ]


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'id': '24de5fe8-985c-4e73-92d4-da015d4beea4'},
            {'status': HTTPStatus.OK},
            {'full_name': 'Caitlin Fowler'},
        ),
        (
            {'id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
            {'status': HTTPStatus.NOT_FOUND},
            {'detail': 'Person not found.'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_person_by_id(
        es_data,
        es_write_to_index,
        make_get_request,
        flush_cache,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_to_index(es_data)
    response = await make_get_request(f'/api/v1/persons/{request_data["id"]}')
    body = await response.json()
    assert response.status == response_data['status']
    assert body.items() >= response_body.items()
