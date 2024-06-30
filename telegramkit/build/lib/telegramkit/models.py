from .base_model import BaseModel
from typing import Optional, List

POST_COUNT = 20 # 

class Post(BaseModel):
    url_template: str = "https://t.me/{channel.url}/{id}"

    def __init__(self, client, channel, id):
        super().__init__(client, id)
        self.channel = channel
        self.html_content = ''
        self.media = []
        self.views = 0
        self.datetime = ''

    async def prior(self) -> Optional["Post"]:
        id = self.channel.get_prior_post_id(self.id)
        if id is None:
            id = self.id - 1
        return await self.channel.get_post(id)

    async def next(self) -> Optional["Post"]:
        id = self.channel.get_next_post_id(self.id)
        if id is None:
            id = self.id + 1
        result = await self.channel.get_post(id)
        return result if result is not None and result.id >= id else None

    # async def get_comments(self, limit=10) -> Optional[List[Comment]]:
    #     from . import telegram_async
    #     return await self.client.get_comments(self, limit)

    # async def get_comment(self, comment_id: int) -> Optional[Comment]:
    #     from . import telegram_async
    #     return await self.client.get_comment(self, comment_id)

    def get_html(self) -> str:
        return self.html_content


class Channel(BaseModel):
    url_template: str = "https://t.me/s/{id}"

    def __init__(self, client, id):
        super().__init__(client, id)
        self.private = False
        self.name = ""
        self.description = ''
        self.subscribers = 0
        self.picture = ''
        self.__posts = {}
    
    def get_html(self) -> str:
        return f"<div><h1>{self.name}</h1><p>{self.description}</p></div>"



    def get_next_post_id(self, post_id: int) -> int:
        result = post_id + 1
        if len(self.__posts) > 0:
            keys = list(self.__posts.keys())
            try:
                index = keys.index(post_id)
                if index < len(keys) - 1:
                    result = keys[index + 1]
            except (ValueError, IndexError):
                pass
        return result

    def get_prior_post_id(self, post_id: int) -> int:
        result = post_id - 1
        if len(self.__posts) > 0:    
            keys = list(self.__posts.keys())
            try:
                index = keys.index(post_id)
                if index > 0:
                    result =  keys[index - 1]
            except (ValueError, IndexError):
                pass
            
        return result if result > 0 else None

    async def get_last_post(self) -> Optional["Post"]:
        self.__posts = await self.client.load_posts(self)
        return list(self.__posts.items())[-1][1] if len(self.__posts) else None

    async def get_post(self, post_id: int) -> Optional[Post]:
        if len(self.__posts) == 0:
            self.__posts = await self.client.load_posts(self, post_id)
        elif post_id not in self.__posts:
            min_id = list(self.__posts.items())[0][0]
            max_id = list(self.__posts.items())[-1][0]
            if post_id < min_id and (min_id - post_id) < POST_COUNT:
                _post_id = min_id - POST_COUNT // 2
            elif post_id > max_id and (post_id - max_id) < POST_COUNT:
                _post_id = max_id + POST_COUNT // 2
            else:
                _post_id = post_id
            self.__posts = await self.client.load_posts(self, _post_id)

        if post_id not in self.__posts:
            return None
        
        return self.__posts[post_id]

    
    async def get_all_posts(self) -> List[Post]:
        return await self.client.get_all_posts(self.id)

    async def is_public(self) -> bool:
        return not self.private

    async def is_private(self) -> bool:
        return self.private




class Media(BaseModel):
    url_template: str = ""

    def __init__(self, client, id):
        super().__init__(client, id)
        self.url = ''
        self.type = ''

    def get_html(self) -> str:
        if self.type.startswith('photo'):
            return f'<img src="{self.url}" alt="photo">'
        elif self.type.startswith('video') or self.type == 'round_video/mp4':
            return f'<video controls><source src="{self.url}" type="{self.type}"></video>'
        elif self.type == 'voice/ogg':
            return f'<audio controls><source src="{self.url}" type="{self.type}"></audio>'
        elif self.type.startswith('audio'):
            return f'<audio controls><source src="{self.url}" type="{self.type}"></audio>'
        elif self.type.startswith('document'):
            return f'<a href="{self.url}">Download document</a>'
        elif self.type.startswith('animation'):
            return f'<video controls loop autoplay><source src="{self.url}" type="{self.type}"></video>'
        else:
            return f'<a href="{self.url}">View file</a>'

class Author(BaseModel):
    url_template: str = "https://t.me/{username}"

    def __init__(self, client, id):
        super().__init__(client, id)
        self.name = ''
        self.username = ''
        self.photo = ''
    
    def get_html(self) -> str:
        return f"<div><h1>{self.name}</h1><p>@{self.username}</p></div>"

class Comment(BaseModel):
    url_template: str = "https://t.me/{post.channel.url}/{post.id}?comment={id}"

    def __init__(self, client, id):
        super().__init__(client, id)
        self.post = None
        self.html_content = ''
        self.reply = None
        self.author = None
        self.datetime = ''

    def get_html(self) -> str:
        return self.html_content
