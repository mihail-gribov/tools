from .base_model import BaseModel

class Comment(BaseModel):
    """Represents a comment with attributes and methods for content management."""
    
    url_template: str = "https://t.me/{post.channel.url}/{post.id}?comment={id}"

    def __init__(self, client, id):
        """Initializes a Comment instance with client and id."""
        super().__init__(client, id)
        self.post = None
        self.html_content = ''
        self.reply = None
        self.author = None
        self.datetime = ''

    def get_html(self) -> str:
        """Returns the HTML content of the comment."""
        return self.html_content
