"""Фикстуры для работы с REST API."""

from typing import Callable

import aiohttp
import pytest
from aiohttp import ClientResponse

from tests.functional.settings import test_settings


@pytest.fixture
def make_get_request() -> Callable:
    """Получить функцию для GET-запросов к API."""
    async def inner(path: str, query_data: dict = {}) -> ClientResponse:
        """Послать GET-запрос REST API.

        Args:
            path: Путь end-point'а.
            query_data: Параметры из строки запроса в URI.

        Returns:
            HTTP-ответ от end-point'а path с заданными параметрами.
        """
        session = aiohttp.ClientSession()
        url = test_settings.api_url + path
        response = await session.get(url, params=query_data)
        await session.close()
        return response
    return inner
