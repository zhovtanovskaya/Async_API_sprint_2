"""Информации о фильтрации данных REST API."""

from pydantic import BaseModel


class FilmFilter(BaseModel):
    """Ограничения, которые клиент REST API накладывает на фильмы."""

    sort: str
    genre: str
