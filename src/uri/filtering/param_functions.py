"""Функции для параметров сортировки и фильтрации в URI."""

from fastapi import Query

from uri.filtering.filters import FilmFilter


def get_film_filter_params(
        sort: str = Query(
            default='',
            title='Сортировка',
            description=(
                'Сортировка принимает значение imdb_rating.'
                '"-" в начале для обратной сортировки'
            ),
            alias='sort',
        ),
        genre: str = Query(
            default='',
            title='Фильтрация по жанру (uuid).',
            alias='filter[genre]',
        ),
        ):
    """Получить объект с сортировкой и фильмов.

    Args:
        sort: Сортировка по названию поля. "-" для сортировки по убыванию.
        genre: uuid жанра, к которому должны принадлежать фильмы.

    Returns:
        Объект FilmFilter.
    """
    return FilmFilter(
        sort=sort,
        filter_genre=genre,
    )
