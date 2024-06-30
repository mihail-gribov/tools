from typing import Optional
from .base_model import BaseModel
from .comment import Comment

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

    async def get_comments(self, limit=10) -> Optional[list[Comment]]:
        if limit <= 0:
            raise ValueError("Limit must be a positive integer")
        try:
            return await self.client.get_comments(self, limit)
        except Exception as e:
            print(f"Failed to get comments: {e}")
            return None

    async def get_comment(self, comment_id: int) -> Optional[Comment]:
        if comment_id <= 0:
            raise ValueError("Comment ID must be a positive integer")
        try:
            return await self.client.get_comment(self, comment_id)
        except Exception as e:
            print(f"Failed to get comment: {e}")
            return None

    def get_html(self) -> str:
        return self.html_content

