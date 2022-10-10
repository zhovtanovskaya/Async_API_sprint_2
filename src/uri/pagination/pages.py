"""Информации о страницах данных REST API."""

from pydantic import BaseModel


class Page(BaseModel):
    """Запрашиваемая клиентом REST API страница данных."""

    number: int
    size: int
