"""Модели персон для сервисов."""

from pydantic.fields import Field

from models.elastic.base_model import ElasticModel


class PersonBase(ElasticModel):
    """Базовый класс для валидации записи индекса 'person'.

    Необходим для вложенного использования в других валидаторах.
    """

    name: str = Field(alias='full_name')
