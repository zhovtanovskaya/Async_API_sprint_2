"""Информации о страницах данных REST API."""

from pydantic import BaseModel, PositiveInt


class Page(BaseModel):
    """Запрашиваемая клиентом REST API страница данных."""

    number: PositiveInt
    size: PositiveInt
