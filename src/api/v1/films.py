"""API для доступа к фильмам."""

import uuid
from http import HTTPStatus

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter

from api.v1.redis_cache import RedisCache
from models.elastic.film import Film
from models.elastic.film_base import FilmBase
from services.abstract import AbstractDetailsService
from services.base import get_film_service
from services.elastic.film import FilmService
from uri.filtering.filters import FilmFilter
from uri.filtering.param_functions import get_film_filter_params
from uri.pagination.pages import Page
from uri.pagination.param_functions import get_page_params

router = APIRouter()


@router.get(
    path='/search',
    response_model=list[FilmBase],
    summary='Поиск фильма по названию.',
    response_description='Ограниченный список фильмов с похожими названиями.',
)
@RedisCache(exclude_kwargs=('film_service',))
async def films_search(
        query: str = Query(
            default='',
            title='Поиск',
            description=(
                'Строка поиска. Поиск по названию '
                'и описанию фильма.'
            ),
            alias='query',
        ),
        page: Page = Depends(get_page_params),
        filter: FilmFilter = Depends(get_film_filter_params),
        film_service: FilmService = Depends(get_film_service),
        ) -> list[FilmBase]:
    """Вернуть список фильмов.

    Args:
        query: Строка поиска.
        filter: Требования к фильтрации и сортировке фильмов.
        film_service: Сервис по получению фильмов.

    Returns:
        Список объектных представлений записей из индекса 'movies'.
    """
    return await film_service.get_films_list(
        page.number,
        page.size,
        filter.sort,
        filter.genre,
        query,
    )


@router.get(
    path='/{film_id}',
    response_model=Film,
    summary='Подробности о фильме.',
    response_description='Детали о фильме и персонах, его создавших.',
)
@RedisCache(exclude_kwargs=('film_service',))
async def film_details(
        film_id: uuid.UUID,
        film_service: AbstractDetailsService = Depends(get_film_service),
        ) -> Film:
    """Получить детали о фильме.

    Args:
        film_id: uuid фильма.
        film_service: сервис по получению фильмов.

    Returns:
        Объектное представление записи из индекса 'movies'.

    Raises:
        HTTPException: С параметром status_code=404, если фильма нет в базе.
    """
    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film


@router.get(
    path='',
    response_model=list[FilmBase],
    summary='Получить одну страницу с фильмами.',
    response_description='Ограниченный список названий и рейтингов фильмов.',
)
@RedisCache(exclude_kwargs=('film_service',))
async def films_list(
        page: Page = Depends(get_page_params),
        filter: FilmFilter = Depends(get_film_filter_params),
        film_service: FilmService = Depends(get_film_service),
        ) -> list[FilmBase]:
    """Вернуть список фильмов.

    Args:
        filter: Требования к фильтрации и сортировке фильмов.
        film_service: Сервис по получению фильмов.

    Returns:
        Список объектных представлений записей из индекса 'movies'.
    """
    return await film_service.get_films_list(
        page.number,
        page.size,
        filter.sort,
        filter.genre,
    )
