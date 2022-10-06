from http import HTTPStatus

import pytest

from tests.functional.src.api_requests import make_get_request
from tests.functional.src.elastic import es_client, es_write_data
from tests.functional.src.redis_cache import redis_client, flush_cache


@pytest.fixture
def es_write_persons(es_write_data):
    return lambda data: es_write_data(data, 'persons')


@pytest.fixture
def es_write_movies(es_write_data):
    return lambda data: es_write_data(data, 'movies')


@pytest.fixture
def es_persons():
    return [
        {
            'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358',
            'name': 'Carrie Fisher',
            'film_ids': [
                '025c58cd-1b7e-43be-9ffb-8571a6135cab',
             ],
            'role': ['actor'],
        },
    ]


@pytest.fixture
def es_movies():
    return [
        {
            'id': '025c58cd-1b7e-43be-9ffb-8571a6135cab',
            'title': 'Star Wars: Episode VI - Return of the Jedi',
            'imdb_rating': 8.3,
            'description': 'Luke Skywalker.',
            'actors': [
                {
                    'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358',
                    'name': 'Carrie Fisher'
                },
            ],
            'director': [],
            'writers': []
        }
    ]


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'person_id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'},
            {'status': HTTPStatus.OK},
            {'full_name': 'Carrie Fisher'},
        ),
        (
            {'person_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'},
            {'status': HTTPStatus.NOT_FOUND},
            {'detail': 'Person not found.'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_person_by_id(
        es_persons,
        es_write_persons,
        make_get_request,
        flush_cache,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_persons(es_persons)
    response = await make_get_request(f'/api/v1/persons/{request_data["person_id"]}')
    body = await response.json()
    assert response.status == response_data['status']
    assert body.items() >= response_body.items()


@pytest.mark.parametrize(
    'request_data, response_data, response_body',
    [
        (
            {'person_id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'},
            {'status': HTTPStatus.OK},
            {'title': 'Star Wars: Episode VI - Return of the Jedi'},
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_person_films(
        es_persons,
        es_movies,
        es_write_persons,
        es_write_movies,
        make_get_request,
        flush_cache,
        request_data,
        response_data,
        response_body,
        ):
    await es_write_persons(es_persons)
    await es_write_movies(es_movies)
    response = await make_get_request(f'/api/v1/persons/{request_data["person_id"]}/films')
    body = await response.json()
    assert response.status == response_data['status']
    assert body[0].items() >= response_body.items()


@pytest.mark.parametrize(
    'query_data, response_data',
    [
        (
            {'query': 'cary fisher'},
            {'status': HTTPStatus.OK},
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(
        es_persons,
        es_write_persons,
        make_get_request,
        flush_cache,
        query_data,
        response_data,
        ):
    await es_write_persons(es_persons)
    response = await make_get_request(f'/api/v1/persons/search', query_data)
    body = await response.json()
    assert response.status == response_data['status']
    assert len(body) > 0