import aiohttp
import pytest

from tests.functional.settings import test_settings


@pytest.fixture
def make_get_request():
    async def inner(path, query_data={}):
        session = aiohttp.ClientSession()
        url = test_settings.api_url + path
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return response
    return inner