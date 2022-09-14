from uuid import UUID

from models.genre_base import GenreBase


class Genre(GenreBase):
    """Объектное представление записи индекса с жанрами в Elastic."""

    description: str | None = ''
    film_ids: list[UUID] = []
