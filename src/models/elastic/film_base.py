from .base_model import DBModel


class FilmBase(DBModel):
    """Базовый валидатор записи индекса 'movies'.

    Необходим для вложенного использования в других валидаторах.
    """

    title: str
    imdb_rating: float | None