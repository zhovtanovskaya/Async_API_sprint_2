"""Модели фильмов для сервисов."""

from .base_model import ElasticModel


class FilmBase(ElasticModel):
    """Базовый валидатор записи индекса 'movies'.

    Необходим для вложенного использования в других валидаторах.
    """

    title: str
    imdb_rating: float | None
