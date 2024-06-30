from typing import Optional
from .base_model import BaseModel
from .post import Post

POST_COUNT = 20 # 

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

    
    async def get_all_posts(self) -> list[Post]:
        return await self.client.get_all_posts(self.id)

    async def is_public(self) -> bool:
        return not self.private

    async def is_private(self) -> bool:
        return self.private

