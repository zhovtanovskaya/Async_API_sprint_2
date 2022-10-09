"""Модели для объектов базы данных, используемых сервисами БД."""

import orjson
from pydantic import BaseModel

from models.abstract import DBModel


def orjson_dumps(v, *, default):
    """Сериалайзер для моделей сервисов."""
    return orjson.dumps(v, default=default).decode()


class ElasticModel(BaseModel, DBModel):
    """Миксин для моделей проекта Movies."""

    id: str

    class Config:
        """Заменяем стандартную работу с json на более быструю."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps

        allow_population_by_field_name = True
