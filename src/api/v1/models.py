"""Модели для формирования ответов от REST API."""
from uuid import UUID

from pydantic import BaseModel


class Film(BaseModel):
    """Объект для возвращения фильма в HTTP-ответе."""
    uuid: UUID
    title: str
    rating: float


class Genre(BaseModel):
    """Объект для возвращения жанра в HTTP-ответе."""
    uuid: UUID
    name: str
    description: str | None
    film_ids: list[UUID]


class Person(BaseModel):
    """Объект для возвращения персоны в HTTP-ответе."""
    uuid: UUID
    full_name: str
    role: list[str]
    film_ids: list[UUID]