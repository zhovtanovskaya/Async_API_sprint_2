"""API для персон."""
from http import HTTPStatus
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query

from models.api.v1.movies import Film, Person
from api.v1.redis_cache import RedisCache
from db.redis import get_redis
from services.abstract import AbstractDetailsService
from services.base import get_film_service, get_person_service
from services.elastic.film import FilmService
from services.elastic.person import PersonService

router = APIRouter()


@router.get('/search', response_model=list[Person])
@RedisCache(exclude_kwargs=('person_service',))
async def search_persons(
        query: str,
        page_number: int = Query(alias="page[number]", default=1, ge=1),
        page_size: int = Query(alias="page[size]", default=50, ge=1),
        person_service: PersonService = Depends(get_person_service),
        redis: Redis = Depends(get_redis),
        ) -> list[Person]:
    """Поиск персон."""
    offset = page_size * (page_number - 1)
    persons = await person_service.search(query, page_size, offset)
    return [Person(uuid=p.id, full_name=p.name, **p.dict()) for p in persons]


@router.get('/{person_id}', response_model=Person)
@RedisCache(exclude_kwargs=('person_service',))
async def person_details(
        person_id: UUID,
        person_service: AbstractDetailsService = Depends(get_person_service),
        redis: Redis = Depends(get_redis),
        ) -> Person | None:
    """Получить персону по идентификатору."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found.')
    return Person(uuid=person.id, full_name=person.name, **person.dict())


@router.get('/{person_id}/film', response_model=list[Film])
@RedisCache(exclude_kwargs=('film_service', 'person_service',))
async def person_films(
        person_id: UUID,
        film_service: FilmService = Depends(get_film_service),
        person_service: PersonService = Depends(get_person_service),
        redis: Redis = Depends(get_redis),
        ) -> list[Film]:
    """Получить список фильмов персоны."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found.')
    films = await film_service.get_by_ids(person.film_ids)
    return [Film(uuid=f.id, title=f.title, rating=f.imdb_rating) for f in films]
