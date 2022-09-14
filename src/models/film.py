from .film_base import FilmBase
from .genre_base import GenreBase
from .person_base import PersonBase


class Film(FilmBase):
    """Валидатор записи индекса 'movies'."""

    description: str | None = ''
    file_link: str | None

    genres: list[GenreBase] = []

    actors: list[PersonBase] = []
    directors: list[PersonBase] = []
    writers: list[PersonBase] = []
