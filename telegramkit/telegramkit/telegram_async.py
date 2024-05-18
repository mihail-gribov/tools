import asyncio
from bs4 import BeautifulSoup
from .http_client import HttpClient
from . import parsers
from .models import Channel, Post, Comment
from .config import request_header


class TelegramClient:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.http_client = HttpClient(loop=self.loop)

    async def fetch_html(self, url: str) -> str:
        return await self.http_client.fetch(url, headers=request_header)

    async def get_channel(self, url: str) -> Channel | None:
        name = url.replace('@', '').split('/')[-1]
        html = await self.fetch_html(f'https://t.me/s/{name}')
        bs = BeautifulSoup(html, 'html.parser')
        info = bs.find(class_='tgme_channel_info')
        return parsers.bs_to_channel(bs, name) if info else None

    async def get_post(self, channel: Channel | str, post_id: int) -> Post | None:
        if isinstance(channel, str):
            channel = await self.get_channel(channel)
        if not channel:
            return None

        html = await self.fetch_html(f'https://t.me/{channel.url.split("/")[-1]}/{post_id}?embed=1')
        bs = BeautifulSoup(html, 'html.parser')
        if bs.find(class_='tgme_widget_message_error'):
            return None
        return parsers.bs_to_post(bs.find(class_='tgme_widget_message'), channel)

    async def get_comments(self, post: Post, limit: int = 10) -> list[Comment] | None:
        html = await self.fetch_html(f'{post.url}?embed=1&discussion=1&comments_limit={limit}')
        bs = BeautifulSoup(html, 'html.parser')
        if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
            return None
        comments = [parsers.bs_to_comments(msg, post) for msg in bs.find_all(class_='tgme_widget_message')]
        comments.reverse()
        return comments

    async def get_comment(self, post: Post, comment_id: int) -> Comment | None:
        html = await self.fetch_html(f'{post.url}?comment={comment_id}&embed=1')
        bs = BeautifulSoup(html, 'html.parser')
        if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
            return None
        return parsers.bs_to_comment(bs.find_all(class_='tgme_widget_message')[0], post)

    async def get_all_posts(self, channel: Channel) -> list[Post]:
        posts = {}
        latest = await channel.get_latest()
        for post in latest:
            posts[post.id] = post

        while True:
            last_pid = sorted(posts.keys())[0]
            url = f'https://t.me/s/{channel.url.split("/")[-1]}/{last_pid}'
            html = await self.fetch_html(url)
            bs = BeautifulSoup(html, 'html.parser')
            for post in bs.find_all(class_='tgme_widget_message'):
                post_object = parsers.bs_to_post(post, channel)
                posts[post_object.id] = post_object
            if 1 in posts:
                break

        return [posts[id] for id in sorted(posts.keys())]
