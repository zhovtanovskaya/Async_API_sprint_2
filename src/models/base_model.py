import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class DBModel(BaseModel):
    """Миксин для моделей проекта Movies."""

    id: str

    class Config:
        """Заменяем стандартную работу с json на более быструю"""

        json_loads = orjson.loads
        json_dumps = orjson_dumps

        allow_population_by_field_name = True
