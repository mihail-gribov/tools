import asyncio
from bs4 import BeautifulSoup
from .http_client import HttpClient
from . import parsers
from .channel import Channel
from .post import Post
from .comment import Comment
from .config import request_header
from typing import Optional

class TelegramClient:
    """Asynchronous Telegram client for fetching channel and post data."""
    
    def __init__(self, loop=None):
        """Initializes a TelegramClient instance with an optional event loop."""
        self.loop = loop or asyncio.get_event_loop()
        self.http_client = HttpClient()

    async def fetch_html(self, url: str) -> str:
        """Fetches HTML content from a given URL asynchronously."""
        html = await self.http_client.fetch(url, headers=request_header)
        if html is None:
            raise ValueError(f"Failed to fetch HTML from {url}")
        return html

    async def get_channel(self, name: str) -> Optional[Channel]:
        """Fetches channel data by name asynchronously."""
        result = Channel(self, name)
        try:
            html = await self.fetch_html(result.get_url())
            bs = BeautifulSoup(html, 'html.parser')
            data = parsers.get_data_channel(bs) if bs else None
            result.from_dict(data)
        except Exception as e:
            print(f"Failed to get channel data: {e}")
            return None
        return result

    async def load_posts(self, channel: Channel, post_id: int = -1) -> list[Post]:
        """Loads posts for a channel asynchronously."""
        url = channel.get_url()
