"""API для персон."""
from http import HTTPStatus
from uuid import UUID

from api.v1.redis_cache import RedisCache
from fastapi import APIRouter, Depends, HTTPException, Query
from models.api.v1.movies import Film, Person
from services.abstract import AbstractDetailsService
from services.base import get_film_service, get_person_service
from services.elastic.film import FilmService
from services.elastic.person import PersonService
from uri.pagination.pages import Page
from uri.pagination.param_functions import get_page_params

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Person],
    summary='Поиск персон по имени.',
    response_description='Список персон с указанием ролей и фильмов каждой.',
)
@RedisCache(exclude_kwargs=('person_service',))
async def search_persons(
        query: str,
        page: Page = Depends(get_page_params),
        person_service: PersonService = Depends(get_person_service),
        ) -> list[Person]:
    """Поиск персон.

    Args:
        query: Текстовый запрос из строки поиска.
        page_number: Номер страницы с результатами поиска.
        page_size: Число совпадений на странице результатов поиска.
        person_service: Сервис для доступа к персонам в БД.
    """
    persons = await person_service.search(query, page.limit, page.offset)
    return [Person(uuid=p.id, full_name=p.name, **p.dict()) for p in persons]


@router.get(
    '/{person_id}',
    response_model=Person,
    summary='Получить персону по идентификатору.',
    response_description='Детали о персоне с указанием ее ролей и фильмов.',
)
@RedisCache(exclude_kwargs=('person_service',))
async def person_details(
        person_id: UUID,
        person_service: AbstractDetailsService = Depends(get_person_service),
        ) -> Person | None:
    """Получить персону по идентификатору.

    Args:
        person_id: Уникальный идентификатор персоны в БД.
        person_service: Сервис для доступа к персонам в БД.

    Raises:
        HTTPException: С параметром status_code=404, если персоны нет в базе.
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Person not found.')
    return Person(uuid=person.id, full_name=person.name, **person.dict())


@router.get(
    '/{person_id}/films',
    response_model=list[Film],
    summary='Получить список фильмов персоны.',
    response_description='Список названий и рейтингов фильмов персоны.',
)
@RedisCache(exclude_kwargs=('film_service', 'person_service',))
async def person_films(
        person_id: UUID,
        film_service: FilmService = Depends(get_film_service),
        person_service: PersonService = Depends(get_person_service),
        ) -> list[Film]:
    """Получить список фильмов персоны.

    Args:
        person_id: Уникальный идентификатор персоны в БД.
        film_service: Сервис для доступа к фильмам в БД.
        person_service: Сервис для доступа к персонам в БД.

    Raises:
        HTTPException: С параметром status_code=404, если персоны нет в базе.
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Person not found.')
    films = await film_service.get_by_ids(person.film_ids)
    return [
        Film(uuid=f.id, title=f.title, rating=f.imdb_rating) for f in films
    ]
