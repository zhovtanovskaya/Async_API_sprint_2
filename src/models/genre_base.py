from .base_model import DBModel


class GenreBase(DBModel):
    """Базовый класс для валидации записи индекса 'genres'.

    Необходим для вложенного использования в других валидаторах.
    """

    name: str
