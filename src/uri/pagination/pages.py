"""Информации о страницах данных."""

from pydantic import BaseModel


class Page(BaseModel):
    """Запрашиваемая клиентом REST API страница данных."""

    number: int
    size: int
