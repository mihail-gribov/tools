from typing import Optional
from .base_model import BaseModel
from .comment import Comment

class Post(BaseModel):
    """Represents a post with attributes and methods for content management."""
    
    url_template: str = "https://t.me/{channel.url}/{id}"

    def __init__(self, client, channel, id):
        """Initializes a Post instance with client, channel, and id."""
        super().__init__(client, id)
        self.channel = channel
        self.html_content = ''
        self.media = []
        self.views = 0
        self.datetime = ''

    async def prior(self) -> Optional["Post"]:
        """Fetches the prior post asynchronously."""
        id = self.channel.get_prior_post_id(self.id)
        if id is None:
            id = self.id - 1
        return await self.channel.get_post(id)

    async def next(self) -> Optional["Post"]:
        """Fetches the next post asynchronously."""
        id = self.channel.get_next_post_id(self.id)
        if id is None:
            id = self.id + 1
        result = await self.channel.get_post(id)
        return result if result is not None and result.id >= id else None

    async def get_comments(self, limit=10) -> Optional[list[Comment]]:
        """Fetches comments for the post asynchronously."""
        if limit <= 0:
            raise ValueError("Limit must be a positive integer")
        try:
            return await self.client.get_comments(self, limit)
        except Exception as e:
            print(f"Failed to get comments: {e}")
            return None

    async def get_comment(self, comment_id: int) -> Optional[Comment]:
        """Fetches a specific comment by its ID asynchronously."""
        if comment_id <= 0:
            raise ValueError("Comment ID must be a positive integer")
        try:
            return await self.client.get_comment(self, comment_id)
        except Exception as e:
            print(f"Failed to get comment: {e}")
            return None

    def get_html(self) -> str:
        """Returns the HTML content of the post."""
        return self.html_content
