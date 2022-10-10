"""Функции для параметров постраничной разбивки в URI."""

from fastapi import Query
from pydantic import PositiveInt

from uri.pagination.pages import Page


def get_page_params(
        page_number: PositiveInt = Query(
            default=1,
            title='Номер страницы',
            alias='page[number]',
        ),
        page_size: PositiveInt = Query(
            default=100,
            title='Размер страницы',
            alias='page[size]',
        ),
        ) -> Page:
    """Функция для параметров страницы из query string в URI.

    Args:
        page_number: Номер страницы, которую хочет получить клиент API.
        page_size: Максимум элементов, которое вернуть клиенту в HTTP-ответе.

    Returns:
        Объект с валидной информацией о странице, полученной из URI.
    """
    return Page(number=page_number, size=page_size)
