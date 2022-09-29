from .base_model import ElasticModel


class GenreBase(ElasticModel):
    """Базовый класс для валидации записи индекса 'genres'.

    Необходим для вложенного использования в других валидаторах.
    """

    name: str
