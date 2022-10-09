"""API для доступа к фильмам."""

import uuid
from http import HTTPStatus

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter
from pydantic import BaseModel

from api.v1.redis_cache import RedisCache
from models.elastic.film import Film
from models.elastic.film_base import FilmBase
from services.abstract import AbstractDetailsService
from services.base import get_film_service
from services.elastic.film import FilmService

router = APIRouter()


class ParamsModel(BaseModel):
    """Модель с общими параметрами для списка фильмов и поиска."""

    page_number: int
    page_size: int
    sort: str
    filter_genre: str


def get_params(
        page_number: int = Query(
            default=1,
            title='Номер страницы',
            alias='page[number]',
        ),
        page_size: int = Query(
            default=100,
            title='Размер страницы',
            alias='page[size]',
        ),
        sort: str = Query(
            default='',
            title='Сортировка',
            description=(
                'Сортировка принимает значение imdb_rating.'
                '"-" в начале для обратной сортировки'
            ),
            alias='sort',
        ),
        filter_genre: str = Query(
            default='',
            title='Фильтрация по жанру (uuid).',
            alias='filter[genre]',
        ),
        ):
    """Получить объект модели с параметрами и описаниями полей запроса.

    Args:
        page_number: Отступ в общем списке фильмов по номеру страницы.
        page_size: Количество фильмов на одной странице.
        sort: Сортировка по названию поля. "-" для сортировки по убыванию.
        filter_genre: uuid жанра, к которому должны принадлежать фильмы.

    Returns:
        Объект ParamsModel.
    """
    return ParamsModel(
        page_size=page_size,
        page_number=page_number,
        sort=sort,
        filter_genre=filter_genre,
    )


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
        params=Depends(get_params),
        film_service: FilmService = Depends(get_film_service),
        ) -> list[FilmBase]:
    """Вернуть список фильмов.

    Args:
        query: Строка поиска.
        params: Общие параметры.
        film_service: Сервис по получению фильмов.

    Returns:
        Список объектных представлений записей из индекса 'movies'.
    """
    return await film_service.get_films_list(
        params.page_number,
        params.page_size,
        params.sort,
        params.filter_genre,
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
        params=Depends(get_params),
        film_service: FilmService = Depends(get_film_service),
        ) -> list[FilmBase]:
    """Вернуть список фильмов.

    Args:
        params: Общие параметры.
        film_service: Сервис по получению фильмов.

    Returns:
        Список объектных представлений записей из индекса 'movies'.
    """
    return await film_service.get_films_list(
        params.page_number,
        params.page_size,
        params.sort,
        params.filter_genre,
    )
