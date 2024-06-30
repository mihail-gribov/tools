from .base_model import BaseModel

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