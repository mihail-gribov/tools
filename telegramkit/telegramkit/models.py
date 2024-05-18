import markdownify
from bs4 import BeautifulSoup
from . import parsers
from . import telegram_async


class Media:
    def __init__(self, url: str, media_type: str) -> None:
        self.url = url
        self.type = media_type

    async def to_dict(self) -> dict:
        return {
            'url': self.url,
            'type': self.type
        }


class Author:
    def __init__(self, name: str, username: str, photo: str) -> None:
        self.name = name
        self.username = username
        self.photo = photo

    async def to_dict(self) -> dict:
        return {
            'name': self.name,
            'username': self.username,
            'photo': self.photo
        }


class Comment:
    def __init__(self, post: 'Post', comment_id: int, text: str, reply: int, author: Author, datetime: str) -> None:
        self.post = post
        self.id = comment_id
        self.text = text
        self.reply = reply
        self.author = author
        self.datetime = datetime

    async def to_dict(self) -> dict:
        return {
            'post': self.post.url,
            'id': self.id,
            'text': self.text,
            'reply': self.reply,
            'author': await self.author.to_dict(),
            'datetime': self.datetime
        }


class Post:
    def __init__(self, channel: 'Channel', url: str, post_id: int, html_content: str, media: list, views: int, datetime: str, data) -> None:
        self.channel = channel
        self.url = url
        self.id = post_id
        self.html_content = html_content
        self.media = media
        self.views = views
        self.datetime = datetime
        self.__data = data

    async def get_comments(self, limit=10) -> list[Comment] | None:
        return await telegram_async.get_comments(self, limit)

    async def get_comment(self, comment_id: int) -> Comment | None:
        return await telegram_async.get_comment(self, comment_id)

    def get_text(self) -> str:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return soup.get_text()

    def get_markdown(self) -> str:
        return markdownify.markdownify(self.html_content)

    def get_links(self) -> list:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]

    async def to_dict(self) -> dict:
        return {
            'channel': self.channel.url,
            'url': self.url,
            'id': self.id,
            'html_content': self.html_content,
            'text': self.get_text(),
            'markdown': self.get_markdown(),
            'links': self.get_links(),
            'media': [await media.to_dict() for media in self.media],
            'views': self.views,
            'datetime': self.datetime
        }


class Channel:
    def __init__(self, url: str, name: str, description: str, subscribers: int, picture: str, data) -> None:
        self.private = False
        self.url = url
        self.name = name
        self.description = description
        self.subscribers = int(subscribers)
        self.picture = picture
        self.__data = data
        self.__posts = {}

    async def get_post(self, post_id: int) -> Post | None:
        return await telegram_async.get_post(self, post_id)

    async def get_latest(self) -> list[Post]:
        return [parsers.bs_to_post(post, self) for post in self.__data.find_all(class_='tgme_widget_message')]

    async def get_all_posts(self) -> list[Post]:
        if not self.__posts:
            self.__posts = await telegram_async.get_all_posts(self)
        return self.__posts

    async def is_public(self) -> bool:
        return not self.private

    async def is_private(self) -> bool:
        return self.private

    async def to_dict(self) -> dict:
        return {
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'subscribers': self.subscribers,
            'picture': self.picture,
            'private': self.private
        }
