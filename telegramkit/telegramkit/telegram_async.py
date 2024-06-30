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
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.http_client = HttpClient()

    async def fetch_html(self, url: str) -> str:
        html = await self.http_client.fetch(url, headers=request_header)
        if html is None:
            raise ValueError(f"Failed to fetch HTML from {url}")
        return html

    async def get_channel(self, name: str) -> Optional[Channel]:
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
        url = channel.get_url()
        if post_id > -1:
            url += f'/{post_id}'
        try:
            html = await self.fetch_html(url)
            bs = BeautifulSoup(html, 'html.parser')
            result = {}
            if bs:
                for data_post in parsers.get_data_posts(bs):
                    id = data_post['id']
                    post = Post(self, channel, id)
                    post.from_dict(data_post)
                    result[id] = post
            return dict(sorted(result.items()))
        except Exception as e:
            print(f"Failed to load posts: {e}")
            return []

    async def get_post(self, channel_id: str, post_id: int) -> Optional[Post]:
        try:
            channel = await self.get_channel(channel_id)
            if not channel:
                return None

            result = Post(self, post_id)
            html = await self.fetch_html(result.get_url())
            bs = BeautifulSoup(html, 'html.parser')
            if bs.find(class_='tgme_widget_message_error'):
                return None

            data = parsers.get_data_post(bs.find(class_='tgme_widget_message'), channel.url)
            result.from_dict(data)
            return result
        except Exception as e:
            print(f"Failed to get post: {e}")
            return None

    async def get_comments(self, post: Post, limit: int = 10) -> Optional[list[Comment]]:
        try:
            html = await self.fetch_html(f'{post.get_url()}?embed=1&discussion=1&comments_limit={limit}')
            bs = BeautifulSoup(html, 'html.parser')
            if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
                return None

            comments = []
            for msg in bs.find_all(class_='tgme_widget_message'):
                comment_id = int(msg.get('data-post-id'))
                result = Comment(self, comment_id)
                data = parsers.get_data_comment(msg, post.get_url())
                result.from_dict(data)
                comments.append(result)

            comments.reverse()
            return comments
        except Exception as e:
            print(f"Failed to get comments: {e}")
            return None

    async def get_comment(self, post: Post, comment_id: int) -> Optional[Comment]:
        try:
            result = Comment(self, comment_id)
            html = await self.fetch_html(f'{post.get_url()}?comment={comment_id}&embed=1')
            bs = BeautifulSoup(html, 'html.parser')
            if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
                return None

            data = parsers.get_data_comment(bs.find_all(class_='tgme_widget_message')[0], post.get_url())
            result.from_dict(data)
            return result
        except Exception as e:
            print(f"Failed to get comment: {e}")
            return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.close()
        if exc_type:
            print(f"Exception raised: {exc_type}, {exc_val}")
        return exc_type is None  # True, если исключение было обработано