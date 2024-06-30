import aiohttp


class HttpClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch(self, url: str, headers: dict = None) -> str:
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()  
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"HTTP request failed: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        if exc_type:
            print(f"Exception raised: {exc_type}, {exc_val}")
        return exc_type is None  
