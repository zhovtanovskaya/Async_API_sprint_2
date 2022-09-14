from pydantic.fields import Field

from models.base_model import DBModel


class PersonBase(DBModel):
    """Базовый класс для валидации записи индекса 'person'.

    Необходим для вложенного использования в других валидаторах.
    """

    name: str = Field(alias='full_name')
