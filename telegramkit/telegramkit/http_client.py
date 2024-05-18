import aiohttp
import asyncio


class HttpClient:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def fetch(self, url: str, headers: dict = None) -> str:
        async with self.session.get(url, headers=headers) as response:
            return await response.text()

    async def close(self):
        await self.session.close()
