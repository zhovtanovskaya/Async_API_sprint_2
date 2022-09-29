"""API для жанров."""

from http import HTTPStatus
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException

from models.api.v1.movies import Genre
from api.v1.redis_cache import RedisCache
from db.redis import get_redis
from services.abstract import AbstractObjectService
from services.base import get_genre_service
from services.elastic.genre import GenreService

router = APIRouter()


@router.get('', response_model=list[Genre])
@RedisCache(exclude_kwargs=('genre_service',))
async def genre_list(
        genre_service: GenreService = Depends(get_genre_service),
        redis: Redis = Depends(get_redis),
        ) -> list[Genre]:
    """Получить список всех жанров."""
    elastic_genres = await genre_service.get_all()
    genres = [Genre(uuid=g.id, **g.dict()) for g in elastic_genres]
    return genres


@router.get('/{genre_id}', response_model=Genre)
@RedisCache(exclude_kwargs=('genre_service',))
async def genre_details(
        genre_id: UUID,
        genre_service: AbstractObjectService = Depends(get_genre_service),
        redis: Redis = Depends(get_redis),
        ) -> Genre | None:
    """Получить жанр по идентификатору."""
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found.')
    return Genre(uuid=genre.id, **genre.dict())
