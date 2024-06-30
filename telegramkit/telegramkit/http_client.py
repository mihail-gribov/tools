import aiohttp

class HttpClient:
    """Asynchronous HTTP client for fetching web content."""
    
    def __init__(self, timeout: int = 10):
        """Initializes an HttpClient instance with a specified timeout."""
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = aiohttp.ClientSession(timeout=self.timeout)

    async def fetch(self, url: str, headers: dict = None) -> str:
        """Fetches the content of a URL asynchronously."""
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
        """Closes the HTTP session asynchronously."""
        await self.session.close()

    async def __aenter__(self):
        """Async context manager entry point."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit point. Closes the session."""
        await self.close()
        if exc_type:
            print(f"Exception raised: {exc_type}, {exc_val}")
        return exc_type is None
