import pytest
import aiohttp
from telegramkit.http_client import HttpClient

@pytest.mark.asyncio
async def test_http_client_fetch_success():
    async with HttpClient() as client:
        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = await client.fetch(url)
        assert response is not None
        assert "userId" in response

@pytest.mark.asyncio
async def test_http_client_fetch_failure():
    async with HttpClient() as client:
        url = "https://invalid.url"
        response = await client.fetch(url)
        assert response is None
