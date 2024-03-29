"""API для жанров."""

from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.redis_cache import RedisCache
from models.api.v1.movies import Genre
from services.abstract import AbstractDetailsService
from services.base import get_genre_service
from services.elastic.genre import GenreService

router = APIRouter()


@router.get(
    '',
    response_model=list[Genre],
    summary='Список жанров.',
    response_description='Список из деталей о жанре и фильмами каждого жанра.',
)
@RedisCache(exclude_kwargs=('genre_service',))
async def genre_list(
        genre_service: GenreService = Depends(get_genre_service),
        ) -> list[Genre]:
    """Получить список всех жанров."""
    elastic_genres = await genre_service.get_all()
    genres = [Genre(uuid=g.id, **g.dict()) for g in elastic_genres]
    return genres


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Подробности о жанре.',
    response_description='Подробности о жанре со списком фильмов этого жанра.',
)
@RedisCache(exclude_kwargs=('genre_service',))
async def genre_details(
        genre_id: UUID,
        genre_service: AbstractDetailsService = Depends(get_genre_service),
        ) -> Genre | None:
    """Получить жанр по идентификатору.

    Raises:
        HTTPException: С параметром status_code=404, если жанра нет в базе.
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found.')
    return Genre(uuid=genre.id, **genre.dict())
