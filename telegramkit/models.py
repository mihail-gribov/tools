import markdownify
from bs4 import BeautifulSoup
from . import parsers
from . import telegram_async

class Media:
    def __init__(self, url, type) -> None:
        self.url = url
        self.type = type

    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'type': self.type
        }

class Author:
    def __init__(self, name, username, photo) -> None:
        self.name = name
        self.username = username
        self.photo = photo

    async def toDict(self) -> dict:
        return {
            'name': self.name,
            'username': self.username,
            'photo': self.photo
        }

class Comment:
    def __init__(self, post, id, text, reply, author, datetime) -> None:
        self.post = post
        self.id = id
        self.text = text
        self.reply = reply
        self.author = author
        self.datetime = datetime

    async def toDict(self) -> dict:
        return {
            'post': self.post.url,
            'id': self.id,
            'text': self.text,
            'reply': self.reply,
            'author': await self.author.toDict(),
            'datetime': self.datetime
        }


class Post:
    def __init__(self, channel, url, id, html_content, media, views, datetime, data) -> None:
        self.channel = channel
        self.url = url
        self.id = id
        self.html_content = html_content
        self.media = media
        self.views = int(views)
        self.datetime = datetime
        self.__data = data

    async def getComments(self, limit=10) -> list[Comment] | None:
        return await telegram_async.getComments(self, limit)

    async def getComment(self, id) -> Comment | None:
        return await telegram_async.getComment(self, id)

    def get_text(self) -> str:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return soup.get_text()

    def get_markdown(self) -> str:
        return markdownify.markdownify(self.html_content)

    def getLinks(self) -> list:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]

    async def toDict(self) -> dict:
        return {
            'channel': self.channel.url,
            'url': self.url,
            'id': self.id,
            'html_content': self.html_content,
            'text': self.get_text(),
            'markdown': self.get_markdown(),
            'links': self.getLinks(),
            'media': [await media.toDict() for media in self.media],
            'views': self.views,
            'datetime': self.datetime
        }


class Channel:
    def __init__(self, url, name, description, subscribers, picture, data) -> None:
        self.private = False
        self.url = url
        self.name = name
        self.description = description
        self.subscribers = int(subscribers)
        self.picture = picture
        self.__data = data
        self.__posts = {}

    async def getPost(self, id: int) -> Post | None:
        return await telegram_async.getPost(self, id)

    async def getLatest(self) -> list[Post]:
        return [parsers.BStoPost(post, self) for post in self.__data.findAll(class_='tgme_widget_message')]

    async def getAllPosts(self) -> list[Post]:
        if not self.__posts:
            self.__posts = await telegram_async.getAllPosts(self)
        return self.__posts

    async def isPublic(self) -> bool:
        return not self.private

    async def isPrivate(self) -> bool:
        return self.private

    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'subscribers': self.subscribers,
            'picture': self.picture,
            'private': self.private
        }
